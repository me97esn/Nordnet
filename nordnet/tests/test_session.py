#!/usr/bin/env python

"""
Unit tests for all session-related stuff

"""

import pprint
import socket
import ssl
import json
from nose.tools import *
from nordnet.restsession import *

def _test_make_hash():
    """ Testing to make a hash-key """
    hashkey = make_hash()
    print hashkey

def _test_connect():
    """ Connecting to the HTTP server """
    connection = connect()

def _test_get_status():
    """ Connecting and getting the accounts """
    connection = connect()
    status = get_status(connection)
    print '\nStatus from server:\n'
    pprint.pprint(status)

def test_get_accounts():
    """ Connecting and getting the accounts """
    session = RestSession()
    accounts = session.get_accounts()
    print "accounts response: %s" % (accounts)
    ok_(accounts[0]['id'], msg='Failed getting accounts from json')
    print '\Accounts from server:\n'

    pprint.pprint(accounts)

def _test_login():
    """ Loggon to the HTTP server """
    hashkey = make_hash()
    connection = connect()
    response = login(connection, hashkey)
    print '\nResult from logon:\n'
    pprint.pprint(response)

#import nose
#nose.run()