import unittest
import requests
import storage
import models

ENDPOINT = 'http://127.0.0.1:5000'


class DataAPI(unittest.TestCase):

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