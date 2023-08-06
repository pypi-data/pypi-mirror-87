import unittest
from server.server import server


class TestServerHandler(unittest.TestCase):
    correct_data = {'response': 200}
    incorrect_data = {
        'response': 400,
        'error': 'Bad Request'
    }

    def test_no_action(self):
        self.assertEqual(server.client_requests_handler(
            {'time': '1.1', 'user': {'account_name': 'Guest'}}), self.incorrect_data)

    def test_wrong_action(self):
        self.assertEqual(server.client_requests_handler(
            {'action': 'post' ,'time': '1.1',  'user': {'account_name': 'Ivan'}}), self.incorrect_data)

    def test_no_time(self):
        self.assertEqual(server.client_requests_handler(
            {'action': 'presence', 'user': {'account_name': 'Guest'}}), self.incorrect_data)

    def test_no_user(self):
        self.assertEqual(server.client_requests_handler(
            {'action': 'presence', 'time': '1.1'}), self.incorrect_data)

    def test_wrong_user(self):
        self.assertEqual(server.client_requests_handler(
            {'action': 'presence','time': '1.1',  'user': {'account_name': 'Ivan'}}), self.incorrect_data)

    def test_correct(self):
        self.assertEqual(server.client_requests_handler(
            {'action': 'presence','time': '1.1',  'user': {'account_name': 'Guest'}}), self.correct_data)




if __name__ == '__main__':
    unittest.main()