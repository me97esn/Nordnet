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
from nordnet.feeds import NordnetSocket

def test_connect_socket_and_rest():
    nordnet_socket = NordnetSocket()
    nordnet_socket.open_socket( nordnet_socket.s )

    session = RestSession()
    accounts = session.get_accounts()
    accounts = session.get_accounts()
    accounts = session.get_accounts()



def test_get_accounts():
    """ Connecting and getting the accounts """
    pprint.pprint("--- Accounts ---")
    session = RestSession()
    accounts = session.get_accounts()
    connection0 = session.connection

    accounts = session.get_accounts()
    ok_(connection0 is session.connection)

    pprint.pprint(accounts)

def test_get_account():
    pprint.pprint("--- Account ---")

    session = RestSession()
    accounts = session.get_accounts()
    account = session.get_account(account_id=accounts[0]['id'])

    pprint.pprint(account)
    ok_(account['accountSum'], msg='Failed getting account sum from json')
    ok_(account['accountCurrency'], msg='Failed getting account currency from json')

    pprint.pprint(accounts)


def test_get_lists():
    pprint.pprint("--- Lists ---")

    session = RestSession()
    lists = session.get_lists(list_id='1')

    #pprint.pprint(lists)

def test_get_positions():
    pprint.pprint("--- Positions ---")
    session = RestSession()
    accounts = session.get_accounts()
    positions = session.get_positions(account_id=accounts[0]['id'])

    pprint.pprint(positions)
    ok_(positions[0]['marketValueAcc'], msg='Failed getting marketValueAcc from json')


def test_get_orders():
    print "--- Orders: ---"

    session = RestSession()
    accounts = session.get_accounts()
    orders = session.get_orders(account_id=accounts[0]['id'])

    pprint.pprint(orders)
    ok_(orders)

def test_logout_and_login():
    print "--- Log in and out: ---"

    """Every call marked with @withAuth should check if session is alive and reconnect otherwise
    """
    session = RestSession()
    ok_(session.get_accounts())
    auth_before_logout = session.auth_headers
    
    # Should not create a new session if still logged in
    session.get_accounts()

    # But after a logout a new session should be created
    session.logout()
    ok_(session.get_accounts()[0]['id'])

    print "session.auth_headers: %s, auth_before_logout:%s" % (session.auth_headers,auth_before_logout)


def test_buy():
    print "--- Buy: ---"

    session = RestSession()
    result = session.buy(volume=1000000, price=64, identifier=101)

    pprint.pprint(result)
    ok_(result['resultCode'], msg='Failed buying a stock')

def test_sell():
    print "--- Sell: ---"

    session = RestSession()

    result = session.sell(volume=1, price=64, identifier=101)

    pprint.pprint(result)
    ok_(result['resultCode'], msg='Failed buying a stock')


