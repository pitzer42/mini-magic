import unittest
import storage

import models


@unittest.skip
class TestBasicStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        storage.reset()

    def test_get_all_cards(self):
        cards = storage.all_cards()
        for card in cards:
            self.assertIsNotNone(card['_id'])
            self.assertIn('cost', card)

    def test_insert_and_get_card(self):
        card = models.create_card(_id='3', name='Vanilla 3', cost=models.create_resources(b=1), attack=1, defense=2,
                                  activated=False)
        storage.insert_card(card)
        other = storage.get_card(card['_id'])
        self.assertIsNotNone(card['_id'])
        self.assertIsNotNone(other['_id'])
        self.assertEqual(card['_id'], other['_id'])
        self.assertEqual(card['cost']['b'], card['cost']['b'])
