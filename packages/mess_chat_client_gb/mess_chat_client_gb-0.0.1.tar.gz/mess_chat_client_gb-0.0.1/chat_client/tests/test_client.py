"""
Unit tests for Chat client side.
"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.config import methods, codes
from client import ChatClient


class TestClient(unittest.TestCase):
    """
    A class of tests for Chat server side
    """
    client = ChatClient
    client.account_name = 'Guest'
    client.status = 'Yep!'

    def test_create_presence_request(self):
        request = self.client.create_presence_request(self.client)

        self.assertTrue(isinstance(request, dict))
        self.assertEqual(request.get("action"), methods.PRESENCE)
        self.assertEqual(request.get("type"), "status")
        self.assertEqual(request.get("user").get("account_name"), 'Guest')
        self.assertEqual(request.get("user").get("status"), 'Yep!')

    def test_response_no_code(self):
        response = {
            "time": int(111),
            "message": "OK"
        }
        self.assertRaises(ValueError, self.client.response_handler, self.client, response)

    def test_response_no_time(self):
        response = {
            "response_code": codes.c200_OK,
            "message": "OK"
        }
        self.assertRaises(ValueError, self.client.response_handler, self.client, response)

    def test_response_no_message(self):
        response = {
            "response_code": codes.c200_OK,
            "time": int(111),
        }
        self.assertRaises(ValueError, self.client.response_handler, self.client, response)

    def test_response_correct(self):
        response = {
            "response_code": codes.c200_OK,
            "time": int(111),
            "message": "OK"
        }
        result = self.client.response_handler(self.client, response)
        self.assertEqual(result, response)


if __name__ == "__main__":
    unittest.main()
