import requests
import urllib.parse
from Settings import Settings

class TgClient:
    base_url = 'https://api.telegram.org/bot{0}/' 
    token = ''
    chat_id = ''

    def __init__(self):
        self.token = Settings().get('token')
        self.chat_id = Settings().get('chat_id')

    def _make_request_url(self, method, params):
        return self.base_url.format(self.token) + method + '?' + urllib.parse.urlencode(params)

    def send_notification(self, message):
        params = {
            'chat_id': self.chat_id,
            'text': message
        }

        url = self._make_request_url('sendMessage', params)

        requests.get(url)

        