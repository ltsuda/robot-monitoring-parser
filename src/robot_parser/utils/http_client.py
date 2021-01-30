import requests
from requests.exceptions import HTTPError
from requests.models import Response


class HTTPClient(object):

    @staticmethod
    def _send(*args):
        response_json = ''
        try:
            response = requests.post(
                args[0]['url'], json=args[0]['payload'], headers=args[0]['headers'])
            response.raise_for_status()
            response_json = response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        else:
            print('Success!')
            return response_json

    @staticmethod
    def login(url, email, password):
        data = {
            'url': str(url),
            'payload': {'email': str(email),
                        'password': str(password)},
            'headers': ''
        }
        token = HTTPClient._send(data)
        return(token['authorization'])

    @staticmethod
    def send_metrics(url, auth_key, payload={}):
        headers = {'Authorization': str(auth_key)}
        data = {
            'url': str(url),
            'payload': payload,
            'headers': headers
        }
        HTTPClient._send(data)
