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

def test_get_accounts():
    """ Connecting and getting the accounts """
    session = RestSession()
    accounts = session.get_accounts()
    print "accounts response: %s" % (accounts)
    ok_(accounts[0]['id'], msg='Failed getting accounts from json')
    print '\Accounts from server:\n'

    pprint.pprint(accounts)

def test_get_account():
    session = RestSession()
    accounts = session.get_accounts()
    account = session.get_account(id=accounts[0]['id'])

    pprint.pprint(account)
    ok_(account['accountCurrency'], msg='Failed getting account from json')

    pprint.pprint(accounts)

def test_buy_ericsson():
    session = RestSession()
    accounts = session.get_accounts()
    account = session.get_account(accounts[0]['id'])

    pprint.pprint(account)
    ok_(account['accountCurrency'], msg='Failed getting account from json')

    pprint.pprint(accounts)

