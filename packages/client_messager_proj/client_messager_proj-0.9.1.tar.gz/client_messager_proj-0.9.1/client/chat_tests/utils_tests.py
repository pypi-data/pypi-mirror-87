# Прежде чем запускать тестирование , необходимо запустить
# файл server.py
# Я пытался запустить ,как отдельный процесс в самом скрипте,
# но регулярно сталкивался с ошибкой :
# ResourceWarning: Enable tracemalloc to get the object allocation traceback
# возможно Вы мне сможете подсказать как ее обойти.


import unittest
from socket import socket, AF_INET, SOCK_STREAM

from server.server.common import utils


class UtilsTest(unittest.TestCase):
    test_message = {
        'action': 'presence',
        'time': 1,
        'user': {
            'account_name': 'Guest'
        }
    }

    def setUp(self):
        #subprocess.Popen([sys.executable, '../server.py'], shell=True)
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.connect(('localhost', 8080))

    def tearDown(self):
        self.client_sock.close()

    def test_get_message(self):
        """Тест обработки сообщения"""
        utils.send_message(self.client_sock, self.test_message)
        self.assertEqual(utils.get_message(client=self.client_sock), {'response': 200})

    def test_send_message(self):
        """ Тест отправки сообщения """
        utils.send_message(self.client_sock, self.test_message)
        self.assertEqual(self.client_sock.recv(1024).decode('utf-8'), '{"response": 200}')

