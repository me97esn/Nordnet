#!/usr/bin/env python

"""
Module for connecting to the REST services of the API
"""

import time
from base64 import b64encode
from M2Crypto import RSA
from httplib import HTTPSConnection, HTTPException
from urllib import urlencode
from json import loads as jloads

from nordnet.config import NordnetConfig, get_logger
from nordnet.utils import print_json

config = NordnetConfig()
logger = get_logger()
no_auth_headers = {
    'Content-type' : 'application/x-www-form-urlencoded',
    'Accept' : 'application/json',
    'Accept-language' : 'en'
    }

# __all__ = ['make_hash', 'connect', 'get_status', 'login']

class withAuth():
    connection = None
    auth_headers = None

    def make_hash(self):
        """ Makes the key for authentication according to the
        specification on Nordnets page """
        timestamp = str(int(round(time.time()*1000)))
        auth = b64encode(config.username) + ':' \
            + b64encode(config.password) + ':' \
            + b64encode(timestamp)
        rsa = RSA.load_pub_key(config.public_key)
        encrypted_auth = rsa.public_encrypt(auth, RSA.pkcs1_padding)
        print 'Made hashkey:'
        key = b64encode(encrypted_auth)
        return key

    def connect(self):
        """ Establishing a connection """
        self.connection = HTTPSConnection(config.url)
        return self.connection

    def login(self):
        hashkey = self.make_hash()
        connection = self.connection or self.connect()

        """ Logs in to the server """
        parameters = urlencode({ 'service' : config.service,
                                 'auth' : hashkey })
        print "parameters for login: '%s'" % (parameters)
        connectionstring = 'https://' + config.base_url + '/' \
            + config.api_version + '/login'

        logger.info('Trying to login to REST: %s' % connectionstring)
        logger.info('Applying header: %s' % no_auth_headers)

        connection.request('POST', connectionstring, parameters, no_auth_headers)

        response = connection.getresponse()
        response_as_json = jloads(response.read())

        basic_auth = b64encode("%s:%s" % (response_as_json['session_key'], response_as_json['session_key']))

        self.auth_headers = no_auth_headers.copy()
        self.auth_headers['Authorization']="Basic %s" %  (basic_auth)

    def __init__(self, f):
        self.decorated_function = f

    def __call__(self):
        # TODO should check if session is alive, and login again if it has timedout
        if self.connection is None:
            self.connect()

        if self.auth_headers is None:
            self.login()


        return self.decorated_function(self) # Prove that function definition has completed

class RestSession():
    config = NordnetConfig()

    @withAuth
    def get_accounts(self):
        """ Gets the server status """
        connectionstring = 'https://' + config.base_url \
            + '/' + config.api_version + '/accounts'

        print "Using auth headers: %s" % (self.auth_headers)
        self.connection.request('GET',
                           connectionstring,
                           '',
                           headers=self.auth_headers)
        response = self.connection.getresponse()
        print "response: %s" % (response)
        logger.info("*"*20)
        return jloads(response.read())

class _RestSession():
    def __init__(self):
        self.http_basic_auth = None
        self.connection = None

    def make_hash(self):
        """ Makes the key for authentication according to the
        specification on Nordnets page """
        timestamp = str(int(round(time.time()*1000)))
        auth = b64encode(config.username) + ':' \
            + b64encode(config.password) + ':' \
            + b64encode(timestamp)
        rsa = RSA.load_pub_key(config.public_key)
        encrypted_auth = rsa.public_encrypt(auth, RSA.pkcs1_padding)
        print 'Made hashkey:'
        key = b64encode(encrypted_auth)
        return key

    def connect(self):
        """ Establishing a connection """
        self.connection = HTTPSConnection(config.url)
        return self.connection

    def get_status(connection):
        """ Gets the server status """
        connectionstring = 'https://' + config.base_url \
            + '/' + config.api_version

        logger.info('Trying to get status: %s' % connectionstring)
        logger.info('Applying header: %s' % headers)

        connection.request('GET', 
                           connectionstring, 
                           '',
                           headers)
        response = connection.getresponse()
        return jloads(response.read())

    def get_accounts(connection):
        """ Gets the server status """
        connectionstring = 'https://' + config.base_url \
            + '/' + config.api_version + '/accounts'

        connection.request('GET',
                           connectionstring,
                           '',
                           headers=headers)
        response = connection.getresponse()
        logger.info("*"*20)
        logger.info("accounts: %s" % (response))
        return jloads(response.read())

    def login(self):
        hashkey = self.make_hash()
        connection = self.connection or self.connect()

        """ Logs in to the server """
        parameters = urlencode({ 'service' : config.service,
                                 'auth' : hashkey })
        print "parameters for login: '%s'" % (parameters)
        connectionstring = 'https://' + config.base_url + '/' \
            + config.api_version + '/login'
        
        logger.info('Trying to login to REST: %s' % connectionstring)
        logger.info('Applying header: %s' % headers)
        
        connection.request('POST', connectionstring, parameters, headers)

        response = connection.getresponse()
        response_as_json = jloads(response.read())

        basic_http_auth = b64encode("%s:%s" % (response_as_json['session_key'], response_as_json['session_key']))
        self.basic_http_auth = basic_http_auth

    def logoff(connection, sessionkey):
        """ Disconnects from the server """
        raise NotImplementedError, 'Logoff-method not implemented.'
