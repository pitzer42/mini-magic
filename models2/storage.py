from pymongo import MongoClient
from models2.entities import Card, Deck, Player, Match, AttrDict


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
        insert_card(models.card(_id=1, name='Vanilla 1', cost=models.resources(a=1), attack=1, defense=1))
        insert_card(models.card(_id=2, name='Vanilla 2', cost=models.resources(b=1), attack=2, defense=1))
        insert_card(models.card(_id=3, name='Mana', cost=models.resources(), effect_id='add_a'))
        insert_card(models.card(_id=4, name='Bolt', cost=models.resources(a=1), effect_id='1_damage'))

        connection.database['Matches'].drop()
        insert_match(models.match(_id=1))

        connection.database['Decks'].drop()
        insert_deck(models.deck(_id=1, card_ids=['1', '2', '4', '3'] * 5))

        connection.database['Players'].drop()
        insert_player(models.player(_id=1))
        insert_player(models.player(_id=2))
        insert_player(models.player(_id=3))


def _all_docs(collection_name):
    with MongoDBConnection() as connection:
        return connection.database[collection_name].find()


def _add_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        data_dict = doc.to_dict()
        result = connection.database[collection_name].insert_one(data_dict)
        doc._id = result.inserted_id


def _get_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        return connection.database[collection_name].find_one({'_id': doc._id})


def _update_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        return connection.database[collection_name].update_one({'_id': str(doc['_id'])}, {'$set': doc})


def update_match(match_dict):
    _update_doc('Matches', match_dict)


def all_cards():
    return [Card(i) for i in _all_docs('Cards')]


def all_decks():
    return [Deck(i) for i in _all_docs('Decks')]


def all_matches():
    return [Match(i) for i in _all_docs('Matches')]


def all_players():
    return [Player(i) for i in _all_docs('Players')]


def insert_card(card):
    _add_doc('Cards', card.to_dict())


def insert_deck(deck):
    _add_doc('Decks', deck.to_dict())


def insert_match(match):
    return _add_doc('Matches', match.to_dict())


def insert_player(player):
    return _add_doc('Players', player.to_dict())


def get_card(card_id):
    data = _get_doc('Cards', card_id)
    return Card(data)


def get_deck(deck_id):
    data = _get_doc('Decks', deck_id)
    return Deck(data)


def get_player(player_id):
    data = _get_doc('Players', player_id)
    return Player(data)


def get_match(match_id):
    data = _get_doc('Matches', match_id)
    return Match(data)


def get_log(match_id):
    match = get_match(match_id).log
    return AttrDict(log=match.log)
