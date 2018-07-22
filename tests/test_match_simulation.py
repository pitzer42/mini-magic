import tests.scenarios as scenarios
from tests.api_test_case import APITestCase
from entities import Match
import events


class TestHappyPath(APITestCase):

    @classmethod
    def setUpClass(cls):
        scenarios.two_players()

    def test(self):
        match_id = self.match_setup()
        self.play_turn(match_id)

    def match_setup(self):
        match_id = self.post_to_create_a_new_match()
        self.post_player_1_setup(match_id)
        self.post_player_2_prompt(match_id)
        return match_id

    def post_to_create_a_new_match(self):
        response = self.assertPost201('/matches')
        self.assertJson(response, '_id')
        match_id = response.json()['_id']
        self.assertGet200('/matches/' + match_id)
        return match_id

    def post_player_1_setup(self, match_id):
        request_data = {'player_id': 1, 'deck_id': 1}
        response = self.assertPost200('/matches/'+match_id+'/join', json=request_data)
        self.assertJson(response, 'players')
        match = Match(response.json())
        players_in_the_match = len(match.players)
        self.assertEqual(players_in_the_match, 1)
        last_event = match.log[-1]['name']
        self.assertEqual(last_event, events.Setup)

    def post_player_2_prompt(self, match_id):
        request_data = {'player_id': 2, 'deck_id': 1}
        response = self.assertPost200('/matches/'+match_id+'/join', json=request_data)
        self.assertJson(response, 'players')
        match = Match(response.json())
        players_in_the_match = len(match.players)
        self.assertEqual(players_in_the_match, 2)
        last_event = match.log[-1]['name']
        self.assertEqual(last_event, events.Prompt)

    def play_turn(self, match_id):
        self.assertPost200('/matches/'+match_id+'/players/1/play/1')
        response = self.assertGet200('/matches/'+match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        cards_in_the_board = len(match.players[0].board)
        self.assertEqual(cards_in_the_board, 1)
        cards_in_hand = len(match.players[0].hand)
        self.assertEqual(cards_in_hand, Match.INITIAL_HAND_SIZE)





