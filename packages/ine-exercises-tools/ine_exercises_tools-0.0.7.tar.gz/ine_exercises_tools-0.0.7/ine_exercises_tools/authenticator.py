import requests


class Authenticator:
    DEV_ENDPOINT_URL = 'https://uaa.development.ine.com/uaa/authenticate'
    PRD_ENDPOINT_URL = 'https://uaa.ine.com/uaa/authenticate'

    @classmethod
    def get_token(cls, username, password, client, development=False):
        if development:
            url = cls.DEV_ENDPOINT_URL
        else:
            url = cls.PRD_ENDPOINT_URL

        response = requests.post(
            url,
            json={
                'username': username,
                'password': password,
                'client': client
            }
        )
        response.raise_for_status()

        try:
            auth_data = response.json()['data']['tokens']['data']['Bearer']
        except KeyError:
            raise RuntimeError('Wrong credentials.')

        return auth_data