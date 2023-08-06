import json
import sys

sys.path.append('../')

def get_message(client):
    """Функция обработки сообщения"""

    encoded_response = client.recv(1024)
    if type(encoded_response) == bytes:
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if type(response) == dict:
            return response
        else:
            raise ValueError
    else:
        raise ValueError

def send_message(sock, message):
    """Функция отправки сообщения в формате json"""

    if not isinstance(message, dict):
        raise ValueError
    js_message = json.dumps(message)
    encoded_message = js_message.encode('utf-8')
    sock.send(encoded_message)