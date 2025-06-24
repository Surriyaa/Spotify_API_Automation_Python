import requests

class SpotifyAPIClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, params=None):
        return requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params)

    def post(self, endpoint, data=None, json=None):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json)

    def delete(self, endpoint, data=None, json=None, params=None):
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json, params=params)