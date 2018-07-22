import unittest
import requests
import storage

ENDPOINT = 'http://127.0.0.1:5000'

@unittest.skip
class TestAPIv2(unittest.TestCase):
    pass

    """
    @classmethod
    def setUpClass(cls):
        storage.reset()
        test_match = models.match(_id='test_match')
        storage.insert_match(test_match)
        test_match = models.match(_id='test_match_2')
        storage.insert_match(test_match)

    def test_get_match_by_id_returns_json(self):
        url = ENDPOINT + '/matches/test_match'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_nonexistent_match_returns_404(self):
        url = ENDPOINT + '/matches/this-match-does-not-exist'
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_log_of_a_match_by_id_returns_json(self):
        url = ENDPOINT + '/matches/test_match/log'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIn('log', response.json())

    def test_post_player_id_and_deck_id_to_join_match(self):
        url = ENDPOINT + '/matches/test_match/join'
        content = {'player_id': '1', 'deck_id': '1'}
        response = requests.post(url, json=content)
        self.assertEqual(response.status_code, 200)
        url = ENDPOINT + '/matches/test_match'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIn('players', response.json())
        players_in_the_match = len(response.json()['players'])
        self.assertGreater(players_in_the_match, 0)

    def test_match_starts_when_have_enough_players(self):
        url = ENDPOINT + '/matches/test_match_2/join'
        content = {'player_id': '1', 'deck_id': '1'}
        response = requests.post(url, json=content)
        self.assertEqual(response.status_code, 200)
        content = {'player_id': '2', 'deck_id': '1'}
        response = requests.post(url, json=content)
        self.assertEqual(response.status_code, 200)
        content = {'player_id': '3', 'deck_id': '1'}
        response = requests.post(url, json=content)
        self.assertEqual(response.status_code, 400)
        self.assertBeginTurnLog()

    def assertBeginTurnLog(self):
        url = ENDPOINT + '/matches/test_match/log'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsNotNone(response_json)
        self.assertIn('log', response_json)
        log = response_json['log']
        self.assertGreater(len(log), 0)
        event = log[0]
        self.assertIn('seq', event)
        self.assertIn('name', event)
        self.assertIn('args', event)
    """



