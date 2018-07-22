from pymongo import MongoClient
from entities import Card, Deck, Player, Match, Resources, AttrDict
from bson import ObjectId


# mongodb://admin:admin123@ds123770.mlab.com:23770/mini-magic
dev_db_uri = 'mongodb://127.0.0.1:27017/mini-magic-db'
dev_db_name = 'mini-magic-db'


class MongoDBConnection(object):

    def __init__(self, uri=dev_db_uri, default_database_name=dev_db_name):
        self.uri = uri
        self.connection = None
        self.default_database_name = default_database_name

    def __enter__(self):
        self.connection = MongoClient(self.uri)
        self.database = self.connection[self.default_database_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def reset():
    with MongoDBConnection() as connection:
        connection.database['Cards'].drop()
        add_card(Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1))
        add_card(Card(_id=2, name='Vanilla 2', cost=Resources(b=1), attack=2, defense=1))
        add_card(Card(_id=3, name='Mana', cost=Resources(), effect_id='add_a'))
        add_card(Card(_id=4, name='Bolt', cost=Resources(a=1), effect_id='1_damage'))

        connection.database['Matches'].drop()
        add_match(Match(_id=1))

        connection.database['Decks'].drop()
        add_deck(Deck(_id=1, card_ids=['1', '2', '4', '3'] * 5))

        connection.database['Players'].drop()
        add_player(Player(_id=1))
        add_player(Player(_id=2))
        add_player(Player(_id=3))


def _drop_all():
    with MongoDBConnection() as connection:
        connection.database['Cards'].drop()
        connection.database['Decks'].drop()
        connection.database['Players'].drop()
        connection.database['Matches'].drop()


def _all_docs(collection_name):
    with MongoDBConnection() as connection:
        result = connection.database[collection_name].find()
        return list(result)


def _add_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        data_dict = doc.to_dict()
        if '_id' in data_dict:
            data_dict['_id'] = doc._id = str(doc._id)
        else:
            data_dict['_id'] = doc._id = str(ObjectId())
        connection.database[collection_name].insert_one(data_dict)
        return data_dict


def _get_doc(collection_name, doc_id):
    with MongoDBConnection() as connection:
        doc_id = str(doc_id)
        return connection.database[collection_name].find_one({'_id': doc_id})


def _update_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        data_dict = doc.to_dict()
        connection.database[collection_name].update_one({'_id': str(doc._id)}, {'$set': data_dict})
        return data_dict


def update_match(match_dict):
    return _update_doc('Matches', match_dict)


def all_cards():
    return _all_docs('Cards')


def all_decks():
    return _all_docs('Decks')


def all_matches():
    return _all_docs('Matches')


def all_players():
    return _all_docs('Players')


def add_card(card):
    return _add_doc('Cards', card)


def add_deck(deck):
    return _add_doc('Decks', deck)


def add_match(match):
    return _add_doc('Matches', match)


def add_player(player):
    return _add_doc('Players', player)


def get_card(card_id):
    return _get_doc('Cards', card_id)


def get_deck(deck_id):
    return _get_doc('Decks', deck_id)


def get_player(player_id):
    return _get_doc('Players', player_id)


def get_match(match_id):
    return _get_doc('Matches', match_id)


def get_log(match_id):
    match = get_match(match_id)
    log = match['log']
    return dict(log=log)
