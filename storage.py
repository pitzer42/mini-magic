from pymongo import MongoClient
import  models
from bson import ObjectId


# "mongodb://admin:admin123@ds123770.mlab.com:23770/mini-magic"
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
        insert_card(models.create_card(_id=1, name='Vanilla 1', cost=models.create_resources(a=1), attack=1, defense=1))
        insert_card(models.create_card(_id=2, name='Vanilla 2', cost=models.create_resources(b=1), attack=2, defense=1))
        insert_card(models.create_card(_id=3, name='Mana', cost=models.create_resources(), attack=0, defense=0))

        connection.database['Matches'].drop()
        insert_match(models.create_match(_id=1))

        connection.database['Decks'].drop()
        insert_deck(models.create_deck(_id=1, card_ids=['1', '1', '1', '2', '2', '3']))

        connection.database['Players'].drop()
        insert_player(models.create_player(_id=1))
        insert_player(models.create_player(_id=2))


def _all_docs(collection_name):
    with MongoDBConnection() as connection:
        docs = list()
        for doc in connection.database[collection_name].find():
            doc['_id'] = str(doc['_id'])
            docs.append(doc)
        return docs


def _add_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        if '_id' in doc and doc['_id'] is None:
            doc['_id'] = ObjectId()
        doc['_id'] = str(doc['_id'])
        connection.database[collection_name].insert_one(doc)


def _get_doc(collection_name, doc_id):
    with MongoDBConnection() as connection:
        return connection.database[collection_name].find_one({'_id': str(doc_id)})


def _update_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        connection.database[collection_name].update_one({'_id': str(doc['_id'])}, {'$set': doc})


def update_match(match_dict):
    _update_doc('Matches', match_dict)


def all_cards():
    return _all_docs('Cards')


def all_decks():
    return _all_docs('Decks')


def all_matches():
    return _all_docs('Matches')


def all_players():
    return _all_docs('Players')


def insert_card(card_dict):
    _add_doc('Cards', card_dict)


def insert_deck(deck_dict):
    _add_doc('Decks', deck_dict)


def insert_match(match_dict):
    return _add_doc('Matches', match_dict)


def insert_player(player_dict):
    return _add_doc('Players', player_dict)


def get_card(card_id):
    return _get_doc('Cards', card_id)


def get_deck(deck_id):
    return _get_doc('Decks', deck_id)


def get_match(match_id):
    return _get_doc('Matches', match_id)


def get_player(player_id):
    return _get_doc('Players', player_id)