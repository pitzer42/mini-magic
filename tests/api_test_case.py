import requests
import unittest


ENDPOINT = 'http://127.0.0.1:5000'


class APITestCase(unittest.TestCase):

    def assertGet200(self, url):
        response = requests.get(ENDPOINT + url)
        self.assertEqual(response.status_code, 200)

    def assertGetJson(self, url):
        response = requests.get(ENDPOINT + url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def assertJsonContains(self, url, *fields):
        response = requests.get(ENDPOINT + url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        for field in fields:
            self.assertIn(field, response_json)
