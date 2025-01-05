import requests
import urllib.parse
from Settings import Settings

class TgClient:
    base_url = 'https://api.telegram.org/bot{0}/' 
    token = ''
    error_chats = []
    chats = []

    def __init__(self):
        self.token = Settings().get('token')
        self.error_chats = Settings().get('error_chats')
        self.chats = Settings().get('chats')

    def _make_request_url(self, method, params):
        return self.base_url.format(self.token) + method + '?' + urllib.parse.urlencode(params)

    def send_chat_notification(self, message, chat_id):
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }

        url = self._make_request_url('sendMessage', params)

        requests.get(url)

    def send_error_notification(self, message):
        for chat_id in self.error_chats:
            self.send_chat_notification(message, chat_id)

    def send_notification(self, message):
        for chat_id in self.chats:
            self.send_chat_notification(message, chat_id)
        