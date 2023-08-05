import unittest
from sys import path as system_path
from os import path, getcwd
system_path.append(path.join(getcwd(), '..'))
from common.CONST import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_answer


class TestClient(unittest.TestCase):
    account_name = 'Guest'
    # def tearDownClass(cls):
    #     inspect.trace(cls)

    def test_def_presense(self):
        test = create_presence(self.account_name)
        test[TIME] = 99.99
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 99.99, USER: {ACCOUNT_NAME: self.account_name}})

    def test_OK_200_answer(self):
        self.assertEqual(process_answer({RESPONSE: 200}), f'Код: 200 Расшифровка: OK')

    def test_Bad_400_answer(self):
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: 'Bad Request'}),
                         f'Ошибка расшифровки с кодом 400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_answer, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
