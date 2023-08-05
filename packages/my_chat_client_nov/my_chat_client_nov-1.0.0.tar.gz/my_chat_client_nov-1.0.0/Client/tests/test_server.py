import unittest
# from logging import getLogger
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
# import logs.server_log_config
from common.CONST import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_message


# SERVER_LOG = getLogger('server')


class TestServer(unittest.TestCase):
    error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok = {RESPONSE: 200}

    def test_no_action(self):
        self.assertEqual(process_client_message(
            {TIME: '99.99', USER: {ACCOUNT_NAME: 'Guest'}}), self.error)

    def test_wrong_action(self):
        self.assertEqual(process_client_message(
            {ACTION: 'Wrong', TIME: '99.99', USER: {ACCOUNT_NAME: 'Guest'}}), self.error)

    def test_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error)

    def test_no_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '99.99'}), self.error)

    def test_unknown_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 99.99, USER: {ACCOUNT_NAME: 'Guest1'}}), self.error)

    def test_ok_check(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 99.99, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok)


if __name__ == '__main__':
    unittest.main()
