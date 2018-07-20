import unittest
import requests
import storage
import models

ENDPOINT = 'http://127.0.0.1:5000'


class TestMiniMagicAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_get_index(self):
        response = requests.get(ENDPOINT)
        self.assertEqual(response.status_code, 200)

    def test_get_cards_as_json(self):
        url = ENDPOINT + '/api/v1.0/cards'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_card_by_id(self):
        url = ENDPOINT + '/api/v1.0/cards/1'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json())
        self.assertIn('cost', response.json())

    def test_get_decks_as_json(self):
        url = ENDPOINT + '/api/v1.0/decks'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_deck_by_id(self):
        url = ENDPOINT + '/api/v1.0/decks/1'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('card_ids', response.json())

    def test_get_matches_as_json(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_match_by_id(self):
        url = ENDPOINT + '/api/v1.0/matches/1'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('_id', response.json())
        self.assertIn('state', response.json())

    def test_post_matches_creates_a_new_match(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertIn('state', response.json())

    def test_post_player_id_and_deck_id_to_match_to_join(self):
        url = ENDPOINT + '/api/v1.0/matches/1'
        response = requests.post(url, json={'player_id': '1', 'deck_id': '1'})
        self.assertEqual(response.status_code, 200)
        url = ENDPOINT + '/api/v1.0/matches/1'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()['players']), 0)

    def test_post_to_match_start(self):
        url = ENDPOINT + '/api/v1.0/matches/1'
        requests.post(url, json={'player_id': '1', 'deck_id': '1'})
        requests.post(url, json={'player_id': '1', 'deck_id': '1'})
        url = ENDPOINT + '/api/v1.0/matches/1/start'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)

        url = ENDPOINT + '/api/v1.0/matches/1'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state'], models.MatchStates.phase_1)
