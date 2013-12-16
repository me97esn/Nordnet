import pprint
import socket
import ssl
import json
import jsonrpclib
import onthestockmarket
from nordnet.restsession import RestBase

import logging

import __main__ as mod_main
import sys, os

sys.path.append('.')

from django.core.management import setup_environ
import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from onthestockmarket.models import *


class NordnetSocket:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.feed_input_handler = FeedInputHandler()
        self.feed_input_handler.handle_data_chunk = self.send_stock_info_to_onthestockmarket


    def send_stock_info_to_onthestockmarket(self, json_str):
        json_obj = json.loads(json_str)
        print "params: %s" % json_obj
        if not json_obj['cmd'] == 'heartbeat':
            logging.info("add_stock_history with params %s" % (json_obj))
            params = json_obj['args']
            identifyer = params["i"]

            try:
                stock = Stock.objects.get(name=identifyer)
                logging.info("Found stock '%s'" % (identifyer))
            except Stock.DoesNotExist, e:
                logging.info("Couldn't find stock with name '%s', creating a new stock" % (identifyer))
                stock = Stock(name=identifyer)
                stock.save()
            history = StockHistory(
                stock=stock,
                bid=params.get('bid'), # Deprecated, should use bid instead

                ask=params.get('ask'),
                ask_volume=params.get('ask_volume'),
                high_price=params.get('high'),
                last_price=params.get('last'),
                lot_size=params.get('lot_size'),
                low_price=params.get('low'),
                open_price=params.get('open'),
                turnover=params.get('turnover'),
                turnover_volume=params.get('turnover_volume'),
                time=params.get('trade_timestamp'),
            )
            history.save()
            logging.info("Stock history %s saved" % (history))
            logging.info("Now, call update() since the stock histories might have changed")
            if hasattr(self, 'takeActionsOnHistory'):
                self.takeActionsOnHistory()

            return 'Done'

    def listen(self):
        ssl_socket = self.open_socket(self.s)
        self.subscribe(
            ['101', '81', '281', '18962', '24235', '34271', '1074', '29375', '85846' '3281', '47', '75712', '24271',
             '4806', '3484', '59064'], ssl_socket)
        print "Reading stream"
        while True:
            output = ssl_socket.read()
            self.handle_output(output)
        print "Closing socket connection..."
        del ssl_socket
        self.s.close()


    def handle_output(self, input):
        "Each message is ended with a newline char. Need to buffer chars"
        print input
        self.feed_input_handler.handle_input(input)

    def open_socket(self, socket):
        rest_base = RestBase()
        response = rest_base.login()

        session_key = response['session_key']
        hostname = response['public_feed']['hostname']
        port = response['public_feed']['port']

        ssl_socket = ssl.wrap_socket(socket)
        ssl_socket.connect((hostname, port))

        cmd = {
            "cmd": "login",
            "args": {
                "session_key": session_key,
                "service": "NEXTAPI"
            }
        }

        num_bytes = ssl_socket.write(json.dumps(cmd) + "\n")
        print "Session key sent (%d bytes)" % num_bytes
        return ssl_socket

    def subscribe(self, identifiers, socket):
        market = 11
        for stock_name in identifiers:
            cmd = {
                "cmd": "subscribe",
                "args": {
                    "t": "price",
                    "m": market,
                    "i": stock_name
                }
            }

            socket.send(json.dumps(cmd) + "\n")


class FeedInputHandler():
    def __init__(self):
        self.buffered_input = ''

    def handle_input(self, input):
        self.buffered_input = self.buffered_input + input
        split_input = self.buffered_input.split('\n')
        complete_chunks = split_input[0:-1]

        for chunk in complete_chunks:
            self.handle_data_chunk(chunk)

        # remove the handled chunks from buffered input
        self.buffered_input = ''.join(split_input[-1:])

    def handle_data_chunk(self, chunk):
        # This methods is overridden elsewhere!
        pass