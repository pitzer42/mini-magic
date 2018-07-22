import tests.scenarios as scenarios
from tests.api_test_case import APITestCase


class TestDataAPI(APITestCase):

    @classmethod
    def setUpClass(cls):
        scenarios.one_of_each_entity()

    def test_get_index(self):
        self.assertGet200('/')

    def test_get_all_cards_as_json(self):
        self.assertGetJson('/cards')

    def test_get_all_decks_as_json(self):
        self.assertGetJson('/decks')

    def test_get_all_players_as_json(self):
        self.assertGetJson('/players')

    def test_get_all_matches_as_json(self):
        self.assertGetJson('/matches')

    def test_get_card_by_id(self):
        self.assertJsonContains('/cards/1', '_id', 'name', 'cost')

    def test_get_deck_by_id(self):
        self.assertJsonContains('/decks/1', '_id', 'card_ids')

    def test_get_match_by_id(self):
        self.assertJsonContains('/matches/1', '_id', 'log')

    def test_get_log_by_match_id(self):
        self.assertJsonContains('/matches/1/log', 'log')
