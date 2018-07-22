import unittest
import requests
import storage


ENDPOINT = 'http://127.0.0.1:5000'


@unittest.skip
class GameAPI(unittest.TestCase):
    pass
    """
    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_regular_match(self):
        match_id = self.create_match()
        self.add_players(match_id)
        self.start(match_id)
        self.draw(match_id)
        self.play(match_id)
        self.next_turn(match_id)
        self.next_turn(match_id)
        self.draw(match_id)
        self.use_card_to_get_resources(match_id)
        self.use_resource_to_play_card_and_use_it_to_deal_damage(match_id)

    def create_match(self):
        url = ENDPOINT + '/api/v1.0/matches'
        response = requests.post(url)
        match = models.match(response.json())
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
        match = models.match(response.json())
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
        field = models.current_player(match)['board']
        self.assertEqual(len(hand), 0)
        self.assertEqual(len(field), 1)

    def use_card_to_get_resources(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/players/1/board/1/use'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        match = storage.get_match(match_id)
        card_in_play = match['players'][0]['board'][0]
        resource_amount = match['players'][0]['resources']['a']
        self.assertTrue(card_in_play['activated'])
        self.assertEqual(resource_amount, 1)

    def next_turn(self, match_id):
        match = storage.get_match(match_id)
        before = match['current_player_index']
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/end_turn'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        match = storage.get_match(match_id)
        after = match['current_player_index']
        self.assertNotEqual(before, after)

    def use_resource_to_play_card_and_use_it_to_deal_damage(self, match_id):
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/players/1/hand/1/play'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
        url = ENDPOINT + '/api/v1.0/matches/' + match_id + '/players/1/board/2/use'
        response = requests.post(url)
        print(response.__dict__)
        self.assertEqual(response.status_code, 200)
        match = storage.get_match(match_id)
        enemy_hp = match['players'][1]['health_points']
        self.assertLess(enemy_hp, 20)
    """