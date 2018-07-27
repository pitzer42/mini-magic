import tests.scenarios as scenarios
from tests.api_test_case import APITestCase
from entities import Match, Player
import events


class TestHappyPath(APITestCase):

    @classmethod
    def setUpClass(cls):
        scenarios.two_players()

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
        self.assertPost200('/matches/'+match_id+'/join', json=request_data)
        response = self.assertGet200('/matches/'+match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        players_in_the_match = len(match.players)
        self.assertEqual(players_in_the_match, 1)
        last_event = match.log[-1]['name']
        self.assertEqual(last_event, events.Setup)

    def post_player_2_prompt(self, match_id):
        request_data = {'player_id': 2, 'deck_id': 2}
        self.assertPost200('/matches/'+match_id+'/join', json=request_data)
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        players_in_the_match = len(match.players)
        self.assertEqual(players_in_the_match, 2)
        last_event = match.log[-1]['name']
        self.assertEqual(last_event, events.Prompt)

    def test_simulated_match(self):
        match_id = self.match_setup()
        self.play_turn_1(match_id)
        self.assertPost200('/matches/' + match_id + '/players/2/end_turn')
        self.play_and_use_counter(match_id)
        self.post_end_turn(match_id)

    def play_turn_1(self, match_id):
        self.post_play_card(match_id)
        self.post_use_card_to_get_resources(match_id)
        self.post_use_resources_to_play_a_card(match_id)
        self.post_use_card_to_deal_damage(match_id)
        self.post_end_turn(match_id)

    def post_play_card(self, match_id):
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        previous_board = len(match.current_player().board)
        previous_hand = len(match.players[0].hand)
        self.assertPost200('/matches/' + match_id + '/players/1/play/1')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        board = len(match.current_player().board)
        self.assertEqual(board, previous_board + 1)
        cards_in_hand = len(match.players[0].hand)
        self.assertEqual(cards_in_hand, previous_hand - 1)
        self.assertPost200('/matches/' + match_id + '/players/2/yield')

    def post_use_card_to_get_resources(self, match_id):
        self.assertPost200('/matches/' + match_id + '/players/1/use/1')
        self.assertPost200('/matches/' + match_id + '/players/2/yield')
        self.assertPost200('/matches/' + match_id + '/players/1/yield')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        resources = match.current_player().resources
        self.assertGreater(resources.a, 0)
        self.assertPost200('/matches/' + match_id + '/players/2/yield')

    def post_use_resources_to_play_a_card(self, match_id):
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        previous_board = len(match.players[0].board)
        self.assertPost200('/matches/' + match_id + '/players/1/play/1')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        resources = match.current_player().resources
        self.assertEqual(resources.a, 0)
        cards_in_the_board = len(match.players[0].board)
        self.assertEqual(cards_in_the_board, previous_board + 1)
        self.assertPost200('/matches/' + match_id + '/players/2/yield')

    def post_use_card_to_deal_damage(self, match_id):
        self.assertPost200('/matches/' + match_id + '/players/1/use/2')
        self.assertPost200('/matches/' + match_id + '/players/2/yield')
        self.assertPost200('/matches/' + match_id + '/players/1/yield')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        enemy = match.players[1]
        self.assertLess(enemy.hp, Player.INITIAL_HP)
        self.assertPost200('/matches/' + match_id + '/players/2/yield')

    def post_end_turn(self, match_id):
        self.assertPost200('/matches/' + match_id + '/players/1/end_turn')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        self.assertEqual(match.current_player_index, 1)

    def play_and_use_counter(self, match_id):
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        previous_hp = match.players[1].hp
        self.assertPost200('/matches/' + match_id + '/players/1/use/2')
        self.assertPost200('/matches/' + match_id + '/players/2/play/1')
        self.assertPost200('/matches/' + match_id + '/players/1/yield')
        self.assertPost200('/matches/' + match_id + '/players/2/use/1')
        self.assertPost200('/matches/' + match_id + '/players/1/yield')
        self.assertPost200('/matches/' + match_id + '/players/2/yield')
        response = self.assertGet200('/matches/' + match_id)
        self.assertJson(response, 'players')
        match = Match(response.json())
        hp = match.players[1].hp
        self.assertEqual(len(match.stack), 0)
        self.assertEqual(previous_hp, hp)



