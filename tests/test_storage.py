import unittest
import storage

from models import Card, Resources, Player, Match, flatten


class TestBasicStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_get_all_cards(self):
        dicts = storage.all_cards()
        cards = Card.create_many(dicts)
        for card in cards:
            self.assertIsNotNone(card._id)
            self.assertEqual(card.__class__, Card)
            self.assertEqual(card.cost.__class__, Resources)

    def test_insert_and_get_card(self):
        card = Card(_id=3, name='Vanilla 3', cost=Resources(b=1), attack=1, defense=2, tapped=False)
        card_dict = flatten(card)
        storage.insert_card(card_dict)
        other_dict = storage.get_card(card._id)
        other = Card.create(other_dict)
        self.assertEqual(other.__class__, Card)
        self.assertEqual(other.cost.__class__, Resources)
        self.assertEqual(card._id, other._id)
        self.assertEqual(card.cost.b, other.cost.b)
