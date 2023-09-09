import requests
import urllib.parse
import json

class TgClient:
    base_url = 'https://api.telegram.org/bot{0}/' 
    token = ''
    chat_id = ''

    def __init__(self):
        with open('token.json', 'r') as token_file:
            data = json.load(token_file)
            self.token = data['token']
            self.chat_id = data['chat_id']

    def _make_request_url(self, method, params):
        return self.base_url.format(self.token) + method + '?' + urllib.parse.urlencode(params)

    def send_notification(self, message):
        params = {
            'chat_id': self.chat_id,
            'text': message
        }

        url = self._make_request_url('sendMessage', params)

        requests.get(url)

        