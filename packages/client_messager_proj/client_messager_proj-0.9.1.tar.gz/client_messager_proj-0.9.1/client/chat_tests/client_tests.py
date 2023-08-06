import unittest
from client.client import client


class TestClient(unittest.TestCase):
    """Класс тестирования"""

    correct_result = {
        'action': 'presence',
        'time': 1,
        'user': {
            'account_name': 'Guest'
        }
    }

    test_create_presence = client.create_presence()
    test_create_presence['time'] = 1

    def test_type_result(self):
        self.assertIsInstance(client.create_presence(), dict)

    def test_correct(self):
        self.assertEqual(self.test_create_presence, self.correct_result)

    def test_response_200(self):
        self.assertEqual(client.server_response_handler({'response': 200}), '200 : OK')

    def test_response_400(self):
        self.assertEqual(client.server_response_handler(
            {'response': 400, 'error': 'Bad Request'}), '400 : Bad Request')



if __name__ == '__main__':
    unittest.main()
