import unittest
import requests
import storage
from models import Match
import json

ENDPOINT = 'http://127.0.0.1:5000'


class TestMiniMagicAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_regular_match(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.post(url)
        match = Match.create(response.json())
        self.assertEqual(match.state, Match.States.waiting_for_players)

        url = ENDPOINT + '/api/v1.0/matches/' + match._id
        response = requests.post(url, json={'player_id': 1, 'deck_id': 1})
        self.assertEqual(response.status_code, 200)
        response = requests.post(url, json={'player_id': 2, 'deck_id': 1})
        self.assertEqual(response.status_code, 200)

        url = ENDPOINT + '/api/v1.0/matches/' + match._id + '/start'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
