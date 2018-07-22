import tests.scenarios as scenarios
from tests.api_test_case import APITestCase


class TestDataAPI(APITestCase):

    @classmethod
    def setUpClass(cls):
        scenarios.one_of_each_entity()

    def test_get_index(self):
        self.assertGet200('/')

    def test_get_all_cards_as_json(self):
        response = self.assertGet200('/cards')
        self.assertJson(response)

    def test_get_all_decks_as_json(self):
        response = self.assertGet200('/decks')
        self.assertJson(response)

    def test_get_all_players_as_json(self):
        response = self.assertGet200('/players')
        self.assertJson(response)

    def test_get_all_matches_as_json(self):
        response = self.assertGet200('/matches')
        self.assertJson(response)

    def test_get_card_by_id(self):
        response = self.assertGet200('/cards/1')
        self.assertJson(response, '_id', 'name', 'cost')

    def test_get_deck_by_id(self):
        response = self.assertGet200('/decks/1')
        self.assertJson(response, '_id', 'card_ids')

    def test_get_match_by_id(self):
        response = self.assertGet200('/matches/1')
        self.assertJson(response, '_id', 'log')

    def test_get_log_by_match_id(self):
        response = self.assertGet200('/matches/1/log')
        self.assertJson(response, 'log')
