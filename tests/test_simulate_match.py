import unittest
import requests
import storage
from models import Match, expand


ENDPOINT = 'http://127.0.0.1:5000'


class TestMiniMagicAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_regular_match(self):
        match_id = self.create_match()
        self.add_players(match_id)
        self.start(match_id)
        self.draw(match_id)

    def create_match(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.post(url)
        match = expand(Match, response.json())
        self.assertIsNotNone(match._id)
        self.assertEqual(match.state, Match.States.waiting_for_players)
        return match._id

    def add_players(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id
        response = requests.post(url, json={'player_id': '1', 'deck_id': '1'})
        self.assertEqual(response.status_code, 200)
        response = requests.post(url, json={'player_id': '2', 'deck_id': '1'})
        self.assertEqual(response.status_code, 200)

    def start(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/start'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        url = ENDPOINT + '/api/v1.0/matches/' + match_id
        response = requests.get(url)
        match = expand(Match, response.json())
        self.assertEqual(match.state, Match.States.phase_1)

    def draw(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/players/1/draw'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cost', response.json())
