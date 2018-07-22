import requests
import unittest


ENDPOINT = 'http://127.0.0.1:5000'


class APITestCase(unittest.TestCase):

    def get(self, url):
        return requests.get(ENDPOINT + url)

    def post(self, url):
        return requests.post(ENDPOINT + url)

    def assertPost200(self, url, json=None):
        response = requests.post(ENDPOINT + url, json=json)
        self.assertEqual(response.status_code, 200)
        return response

    def assertPost201(self, url):
        response = requests.post(ENDPOINT + url)
        self.assertEqual(response.status_code, 201)
        return response

    def assertGet200(self, url):
        response = requests.get(ENDPOINT + url)
        self.assertEqual(response.status_code, 200)
        return response

    def assertJson(self, response, *fields):
        response_json = response.json()
        self.assertIsNotNone(response_json)
        for field in fields:
            self.assertIn(field, response_json)
