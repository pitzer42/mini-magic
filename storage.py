from pymongo import MongoClient
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


def drop_all():
    with MongoDBConnection() as connection:
        connection.database['Cards'].drop()
        connection.database['Decks'].drop()
        connection.database['Players'].drop()
        connection.database['Matches'].drop()


def drop(collection_name):
    with MongoDBConnection() as connection:
        connection.database[collection_name].drop()


def all_docs(collection_name):
    with MongoDBConnection() as connection:
        result = connection.database[collection_name].find()
        return list(result)


def get_doc(collection_name, doc_id):
    with MongoDBConnection() as connection:
        doc_id = str(doc_id)
        return connection.database[collection_name].find_one({'_id': doc_id})


def save_doc(collection_name, doc):
    with MongoDBConnection() as connection:
        if '_id' in doc and doc['_id']:
            doc['_id'] = str(doc['_id'])
        else:
            doc['_id'] = str(ObjectId())
        connection.database[collection_name].replace_one(dict(_id=doc['_id']), doc, upsert=True)
        return doc['_id']
