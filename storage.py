from pymongo import MongoClient
from bson import json_util
import json

MATCH_STATE_ERROR = 'forbidden operation'


def reset_database():
    decks = [
        {'_id': 0, 'cards': [1, 1, 2, 2, 1, 2, 2]},
        {'_id': 1, 'cards': [2, 2, 1, 1, 2, 1, 1]},
    ]

    cards = [
        {
            '_id': 1,
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
            '_id': 2,
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

    matches = [{'_id': 1, 'state': 'waiting_players'}]

    with MongoDBConnection() as connection:
        def reset_collection(collection_name, new_items):
            collection = connection.database[collection_name]
            collection.drop()
            for item in new_items:
                collection.insert_one(item)

        reset_collection('cards', cards)
        reset_collection('decks', decks)
        reset_collection('matches', matches)


class MongoDBConnection(object):

    def __init__(self, uri="mongodb://admin:admin123@ds123770.mlab.com:23770/mini-magic", default_database_name='mini-magic'):
        self.uri = uri
        self.connection = None
        self.default_database_name = default_database_name

    def __enter__(self):
        self.connection = MongoClient(self.uri)
        self.database = self.connection[self.default_database_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def list_cards():
    with MongoDBConnection() as connection:
        result = list()
        all_cards = connection.database['cards'].find()
        for card in all_cards:
            card_json = json.loads(json_util.dumps(card))
            result.append(card_json)
        return result


def get_card(card_id):
    with MongoDBConnection() as connection:
        card = connection.database['cards'].find_one({'_id': card_id})
        return json.loads(json_util.dumps(card))


def list_decks():
    with MongoDBConnection() as connection:
        result = list()
        all_decks = connection.database['decks'].find()
        for deck in all_decks:
            deck_json = json.loads(json_util.dumps(deck))
            result.append(deck_json)
        return result


def get_deck(deck_id):
    with MongoDBConnection() as connection:
        deck = connection.database['decks'].find_one({'_id': deck_id})
        return json.loads(json_util.dumps(deck))


def create_match():
    with MongoDBConnection() as connection:
        match = dict()
        match['state'] = 'waiting_players'
        connection.database['matches'].insert(match)
        return json.loads(json_util.dumps(match))


def list_matches():
    with MongoDBConnection() as connection:
        result = list()
        all_matches = connection.database['matches'].find()
        for match in all_matches:
            match_json = json.loads(json_util.dumps(match))
            result.append(match_json)
        return result


def get_match(match_id):
    with MongoDBConnection() as connection:
        match = connection.database['matches'].find_one({'_id': match_id})
        return json.loads(json_util.dumps(match))


def add_player_to_match(match_id, player_id, deck_id):
    with MongoDBConnection() as connection:
        match = connection.database['matches'].find_one({'_id': match_id})
        if match['state'] != 'waiting_players':
            raise MATCH_STATE_ERROR
        player = {'_id': player_id, 'deck_id': deck_id}
        if 'players' not in match:
            match['players'] = list()
        match['players'].append(player)
        connection.database['matches'].update_one({'_id': match_id}, {'$set': match})
        return json.loads(json_util.dumps(match))


def start_match(match_id):
    with MongoDBConnection() as connection:
        match = connection.database['matches'].find_one({'_id': match_id})
        if match['state'] != 'waiting_players':
            raise MATCH_STATE_ERROR
        match['state'] = 'phase_1'
        match['current_player'] = match['players']['_id']
        connection.database['matches'].update_one({'_id': match_id}, {'$set': match})
        return json.loads(json_util.dumps(match))


def draw(match_id, player_id):
    with MongoDBConnection() as connection:
        match = connection.database['matches'].find_one({'_id': match_id})
        if match['state'] != 'phase_1':
            raise MATCH_STATE_ERROR
        if match['current_player'] != player_id:
            raise MATCH_STATE_ERROR
        for player in match['players']:
            if player['_id'] == player_id:
                top_card = player['deck']['cards'].pop()
                player['hand'].append(top_card)
                break
        connection.database['matches'].update_one({'_id': match_id}, {'$set': match})
        return json.loads(json_util.dumps(match))



