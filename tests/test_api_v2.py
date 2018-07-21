import unittest
import requests
import storage
import models

ENDPOINT = 'http://127.0.0.1:5000'


class TestAPIv2(unittest.TestCase):

    def assert_get_url(self, url, expected_status=200):
        response = requests.get(ENDPOINT + url)
        self.assertEqual(response.status_code, expected_status)
        return response

    @classmethod
    def setUpClass(cls):
        storage.reset()
        test_match = models.match(_id='test_match')
        storage.insert_match(test_match)
        test_match = models.match(_id='test_match_2')
        storage.insert_match(test_match)

    def test_get_match_by_id_returns_json(self):
        response = self.assert_get_url('/matches/test_match')
        self.assertIsNotNone(response.json())

    def test_get_nonexistent_match_returns_404(self):
        self.assert_get_url('/matches/this-match-does-not-exist', expected_status=404)

    def test_get_log_of_a_match_by_id_returns_json(self):
        response = self.assert_get_url('/matches/test_match/log')
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

    def test_cannot_play_without_enough_resources(self):
        url = ENDPOINT + '/matches/test_match_2/players/1/play/1'
        response = requests.post(url)
        self.assertEqual(response.status_code, 400)

    def test_simulation(self):
        url = ENDPOINT + '/matches/test_match_3'
        requests.post(url)
        url = ENDPOINT + '/matches/test_match_3/join'
        content = {'player_id': '1', 'deck_id': '1'}
        requests.post(url, json=content)
        content = {'player_id': '2', 'deck_id': '1'}
        requests.post(url, json=content)

        url = ENDPOINT + '/matches/test_match_3/players/1/play/1'
        requests.post(url)

        url = ENDPOINT + '/matches/test_match_3/players/1/use/1'
        requests.post(url)

        url = ENDPOINT + '/matches/test_match_3'
        response = requests.get(url)
        match = response.json()
        card_in_play = match['players'][0]['board'][0]
        resources = match['players'][0]['resources']
        self.assertTrue(card_in_play['activated'])
        self.assertGreater(resources['a'], 0)

        url = ENDPOINT + '/matches/test_match_3/players/1/yield'
        requests.post(url)

        url = ENDPOINT + '/matches/test_match_3'
        response = requests.get(url)
        match = response.json()
        turn_end_event = [e for e in match['log'] if e['name'] == models.Events.TurnEnd]
        self.assertIsNotNone(turn_end_event)
        self.assertGreater(len(turn_end_event), 0)


