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
import requests
import json
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

class RestBase():
    connection = None
    auth_headers = None
    marketID = 11
    currency = 'SEK'
    auth_session_key = None

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
        self.auth_session_key = response_as_json['session_key']

        basic_auth = b64encode("%s:%s" % (self.auth_session_key, self.auth_session_key))

        self.auth_headers = no_auth_headers.copy()
        self.auth_headers['Authorization']="Basic %s" %  (basic_auth)
        return response_as_json

    def post(self, relative_url='/', data={}):
        url = 'https://%s/%s%s' % (config.base_url,config.api_version, relative_url)

        r = requests.post(url,
                      data=data,
                      headers=self.auth_headers
        ).text
        return json.loads(r)


    def request(self, relative_url='/', method='GET', ):
        connectionstring = 'https://' + config.base_url \
            + '/' + config.api_version + relative_url

        self.connection.request(method,
                           connectionstring,
                           '',
                           headers=self.auth_headers)
        response = self.connection.getresponse()
        return jloads(response.read())

class withAuth(RestBase):
    

    def __init__(self, f):
        self.decorated_function = f

    def __call__(self, **kwargs):
        if self.auth_session_key:
            logged_in_response = self.request(method='PUT', relative_url="/login/%s" % self.auth_session_key)
            if not logged_in_response['logged_in']:
                # Set auth stuff to None so that a new session is created
                self.connection = None
                self.auth_headers = None
                self.auth_session_key = None

        if self.connection is None:
            self.connect()

        if self.auth_headers is None:
            self.login()

        return self.decorated_function(self, **kwargs)

class RestSession(RestBase):
    config = NordnetConfig()

    @withAuth
    def get_accounts(self, **kwargs):
        return self.request(method='GET', relative_url='/accounts')

    @withAuth
    def logout(self, **kwargs):
        return self.request(method='DELETE', relative_url="/login/%s" % self.auth_session_key)

    @withAuth
    def get_account(self, **kwargs):
        return self.request(method='GET', relative_url='/accounts/' + kwargs['account_id'])

    @withAuth
    def get_orders(self, **kwargs):
        return self.request(method='GET', relative_url="/accounts/%s/orders" % (kwargs['account_id']))

    @withAuth
    def get_positions(self, **kwargs):
        return self.request(method='GET', relative_url="/accounts/%s/positions" % (kwargs['account_id']))

    @withAuth
    def buy(self, **kwargs):
        data = {'identifier': kwargs['identifier'], 'marketID': self.marketID, 'price': kwargs['price'],
                       'volume': kwargs['volume'], 'currency': self.currency, 'side': 'buy'}
        url = '/accounts/%s/orders' % config.account_id

        print "posting %s to %s" % (data, url)

        return self.post(relative_url=url,
                         data=data)
    @withAuth
    def sell(self, **kwargs):
        data = {'identifier': kwargs['identifier'], 'marketID': self.marketID, 'price': kwargs['price'],
                       'volume': kwargs['volume'], 'currency': self.currency, 'side': 'sell'}
        url = '/accounts/%s/orders' % config.account_id

        print "posting %s to %s" % (data, url)

        return self.post(relative_url=url,
                         data=data)

