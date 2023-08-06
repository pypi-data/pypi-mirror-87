"""
Unit tests for Chat server side.
"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import ChatServer
from common.config import methods, codes


class TestServer(unittest.TestCase):
    """
    A class of tests for Chat server side
    """

    server = ChatServer()

    def test_request_no_action(self):
        request = {
            "time": int(111),
            "type": "status",
            "user": {
                "account_name": "Guest",
                "status": "Yep!"
            }

        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c400_WRONG_REQUEST)
        self.assertEqual(response.get("message"), "Unsupported action")

    def test_request_wrong_action(self):
        request = {
            "action": "wrong",
            "time": int(111),
            "type": "status",
            "user": {
                "account_name": "Guest",
                "status": "Yep!"
            }

        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c400_WRONG_REQUEST)
        self.assertEqual(response.get("message"), "Unsupported action")

    def test_request_no_time(self):
        request = {
            "action": methods.PRESENCE,
            "type": "status",
            "user": {
                "account_name": "Guest",
                "status": "Yep!"
            }

        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c400_WRONG_REQUEST)
        self.assertEqual(response.get("message"), "Wrong message's fields")

    def test_request_no_type(self):
        request = {
            "action": methods.PRESENCE,
            "time": int(111),
            "user": {
                "account_name": "Guest",
                "status": "Yep!"
            }

        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c400_WRONG_REQUEST)
        self.assertEqual(response.get("message"), "Wrong message's fields")

    def test_request_no_user(self):
        request = {
            "action": methods.PRESENCE,
            "time": int(111),
            "type": "status"
        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c400_WRONG_REQUEST)
        self.assertEqual(response.get("message"), "Wrong message's fields")

    def test_request_correct(self):
        request = {
            "action": methods.PRESENCE,
            "time": int(111),
            "type": "status",
            "user": {
                "account_name": "Guest",
                "status": "Yep!"
            }

        }
        response = self.server.request_handler(request)
        self.assertEqual(response.get("response_code"), codes.c200_OK)
        self.assertEqual(response.get("message"), "OK")


if __name__ == "__main__":
    unittest.main()
