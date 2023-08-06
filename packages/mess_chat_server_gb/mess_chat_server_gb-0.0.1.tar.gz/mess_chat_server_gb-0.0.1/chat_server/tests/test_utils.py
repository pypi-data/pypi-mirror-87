"""
Unit tests for Utils.
"""


import json
import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.config import network, methods, codes
from common.utils import get_message, send_message

UNIVERSAL_MESSAGE = {
    "action": methods.PRESENCE,
    "time": int(111),
    "type": "status",
    "user": {
        "account_name": "Guest",
        "status": "Yep!"
    },
    "response_code": codes.c400_WRONG_REQUEST,
    "message": "Unsupported action"

}


class MockSocket:
    """
    A mock soket class
    """

    def __init__(self):
        self.in_socket_message = None

    def send(self, message):
        assert isinstance(message, bytes)
        self.in_socket_message = message

    def recv(self, max_length):
        assert isinstance(max_length, int)
        return json.dumps(UNIVERSAL_MESSAGE).encode(encoding=network.ENCODING)

    def get_in_socket_message(self):
        return self.in_socket_message.decode(encoding=network.ENCODING)


class TestUtils(unittest.TestCase):
    """
    A class of tests for utils
    """

    socket = MockSocket()

    def test_send_message(self):
        send_message(self.socket, UNIVERSAL_MESSAGE)
        self.assertEqual(json.dumps(UNIVERSAL_MESSAGE), self.socket.get_in_socket_message())

    def test_get_message(self):
        data = get_message(self.socket)
        self.assertEqual(UNIVERSAL_MESSAGE, data)


if __name__ == "__main__":
    unittest.main()
