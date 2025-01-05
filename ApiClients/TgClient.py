import requests
import urllib.parse
import logging
from Settings import Settings

class TgClient:
    logger = logging.getLogger()
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

    def send_chat_notification(self, message, chat_id, parse_mode='MarkdownV2'):
        params = {
            'chat_id': chat_id,
            'text': message,
        }

        if parse_mode != None:
            params['parse_mode'] = parse_mode

        url = self._make_request_url('sendMessage', params)

        return requests.get(url)

    def send_error_notification(self, message, parse_mode='MarkdownV2'):
        for chat_id in self.error_chats:
            response = self.send_chat_notification(message, chat_id, parse_mode)

            if response.status_code != 200:
                self._log_send_error('send_error_notification', chat_id, response.status_code, response.text, message)

    def send_notification(self, target_chat_id, message):
        response = self.send_chat_notification(message, target_chat_id)

        if response.status_code != 200:
                self._log_send_error('send_notification', target_chat_id, response.status_code, response.text, message)

        chats = self.chats.copy()

        if target_chat_id in chats: chats.remove(target_chat_id)

        for chat_id in chats:
            response = self.send_chat_notification(message, chat_id)

            if response.status_code != 200:
                self._log_send_error('send_notification', chat_id, response.status_code, response.text, message)
                self.send_error_notification(f"🆘 status code: {response.status_code}\nresponse: {response.text}", parse_mode=None)
    
    def _log_send_error(self, method, chat_id, status_code, response, message):
        self.logger.error(f"""
{method}
chat_id: {chat_id}
status_code: {status_code}
response: {response}
msg: {message}""")