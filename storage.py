decks = [
    [1, 1, 1],
    [1, 2, 2],
]

cards = [
    {
        'id': 0,
        'name': 'Vanilla 0',
        'cost':
            {
                'a': 1,
                'b': 0,
                'c': 0
             },
        'attack': 1,
        'defense': 1,
        'tapped': False
    },
    {
        'id': 1,
        'name': 'Vanilla 1',
        'cost':
            {
                'a': 1,
                'b': 1,
                'c': 0
             },
        'attack': 2,
        'defense': 2,
        'tapped': False
    }
]

DATABASE_URI = "mongodb://admin:admin123@ds123770.mlab.com:23770/mini-magic"

from pymongo import MongoClient


def setup():
    pass
    client = MongoClient(DATABASE_URI)
    db = client['mini-magic']
    cards[0]['id'] = db['cards'].insert_one(cards[0])
    cards[1]['id'] = db['cards'].insert_one(cards[1])


def list_cards():
    return cards


def get_card(card_id):
    result = [card for card in cards if card['id'] == card_id]
    if len(result) > 0:
        return result[0]
    return None


def list_decks():
    return decks


def get_deck(deck_id):
    if deck_id < 0 or deck_id >= len(decks):
        return None
    return decks[deck_id]


def create_match(new_match):
    return 1


def get_match(match_id):
    return {'id': match_id, 'hand': []}


def draw(match, player_id):
    pass

