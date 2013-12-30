import pprint
import socket
import ssl
import json
import jsonrpclib

from nordnet.restsession import RestBase, RestSession

import logging

import __main__ as mod_main

class NordnetSocket:
    def __init__(self, rest_session = None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.feed_input_handler = FeedInputHandler()
        self.feed_input_handler.handle_data_chunk = lambda : None
        self.rest_session = rest_session


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
        session_key = self.rest_session.auth_session_key
        hostname = self.rest_session.auth_hostname
        port = self.rest_session.auth_port

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