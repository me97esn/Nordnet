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
    account = session.get_account(account_id=accounts[0]['id'])

    pprint.pprint(account)
    ok_(account['accountSum'], msg='Failed getting account sum from json')
    ok_(account['accountCurrency'], msg='Failed getting account currency from json')

    pprint.pprint(accounts)

def test_get_orders():
    session = RestSession()
    accounts = session.get_accounts()
    orders = session.get_orders(account_id=accounts[0]['id'])

    print "Result:"
    pprint.pprint(orders)
    ok_(orders)


def test_buy():
    session = RestSession()
    result = session.buy(volume=1, price=64, identifier=101)

    pprint.pprint(result)
    ok_(result['resultCode'], msg='Failed buying a stock')

def test_sell():
    session = RestSession()

    result = session.sell(volume=1, price=64, identifier=101)

    pprint.pprint(result)
    ok_(result['resultCode'], msg='Failed buying a stock')


