from pymongo import MongoClient
from models import Match, Card, Resources, Deck, Player, flatten
from bson import ObjectId


# "mongodb://admin:admin123@ds123770.mlab.com:23770/mini-magic"
dev_db_uri = 'mongodb://127.0.0.1:27017/mini-magic-db'


class MongoDBConnection(object):

    def __init__(self, uri=dev_db_uri, default_database_name='mini-magic-db'):
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
        insert_card(flatten(Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1, tapped=False)))
        insert_card(flatten(Card(_id=2, name='Vanilla 2', cost=Resources(b=1), attack=2, defense=1, tapped=False)))

        connection.database['Matches'].drop()
        insert_match(flatten(Match(_id=1)))

        connection.database['Decks'].drop()
        insert_deck(flatten(Deck(_id=1, cards=['1', '1', '1', '2', '2', '2'])))

        connection.database['Players'].drop()
        insert_player(flatten(Player(_id=1)))
        insert_player(flatten(Player(_id=2)))


def all_docs(collection_name):
    with MongoDBConnection() as connection:
        docs = list()
        for doc in connection.database[collection_name].find():
            doc['_id'] = str(doc['_id'])
            docs.append(doc)
        return docs


def insert_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        if '_id' in doc and doc['_id'] is None:
            doc['_id'] = ObjectId()
        doc['_id'] = str(doc['_id'])
        connection.database[collection_name].insert_one(doc)


def get_doc(collection_name, doc_id):
    with MongoDBConnection() as connection:
        return connection.database[collection_name].find_one({'_id': str(doc_id)})


def update_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        connection.database[collection_name].update_one({'_id': str(doc['_id'])}, {'$set': doc})


def update_match(match_dict):
    update_doc('Matches', match_dict)


def all_cards():
    return all_docs('Cards')


def all_decks():
    return all_docs('Decks')


def all_matches():
    return all_docs('Matches')


def all_players():
    return all_docs('Players')


def insert_card(card_dict):
    insert_doc('Cards', card_dict)


def insert_deck(deck_dict):
    insert_doc('Decks', deck_dict)


def insert_match(match_dict):
    return insert_doc('Matches', match_dict)


def insert_player(player_dict):
    return insert_doc('Players', player_dict)


def get_card(card_id):
    return get_doc('Cards', card_id)


def get_deck(deck_id):
    return get_doc('Decks', deck_id)


def get_match(match_id):
    return get_doc('Matches', match_id)


def get_player(player_id):
    return get_doc('Players', player_id)