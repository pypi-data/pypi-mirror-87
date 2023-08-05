import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.CONST import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import get_message, send_message


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, messege_sent):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = messege_sent

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    account_name = 'Guest'
    messege_sent = {
        ACTION: PRESENCE,
        TIME: 99.99,
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    recieve_ok = {RESPONSE: 200}
    recieve_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message(self):
        test_socket = TestSocket(self.messege_sent)
        send_message(test_socket, self.messege_sent)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        ok = TestSocket(self.recieve_ok)
        err = TestSocket(self.recieve_error)
        self.assertEqual(get_message(ok), self.recieve_ok)
        self.assertEqual(get_message(err), self.recieve_error)


if __name__ == '__main__':
    unittest.main()
