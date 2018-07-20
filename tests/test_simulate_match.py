import unittest
import requests
import storage
import models


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
        self.play(match_id)

    def create_match(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.post(url)
        match = models.create_match(response.json())
        self.assertIsNotNone(match['_id'])
        self.assertEqual(match['state'], models.MatchStates.waiting_for_players)
        return match['_id']

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
        match = models.create_match(response.json())
        self.assertEqual(match['state'], models.MatchStates.phase_1)

    def draw(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/draw'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        match = storage.get_match(match_id)
        hand = models.current_player(match)['hand']
        self.assertGreater(len(hand), 0)

    def play(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/players/1/hand/1/play'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        match = storage.get_match(match_id)
        hand = models.current_player(match)['hand']
        field = models.current_player(match)['field']
        self.assertEqual(len(hand), 0)
        self.assertEqual(len(field), 1)
