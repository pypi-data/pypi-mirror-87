from pymongo import MongoClient
from os import getenv

MONGO_URL = getenv('MONGO_URL')
MONGO_DB = getenv('MONGO_DB')


def singleton(my_class):
    instances = dict()

    def get_instances(*args, **kwargs):
        if my_class not in instances:
            instances[my_class] = my_class(*args, *kwargs)
        return instances[my_class]

    return get_instances


@singleton
class ConnectMongo(object):

    def __init__(self):
        self.client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        self.db = self.client[MONGO_DB]
        self.error_collection = self.db['error']
        self.info_collection = self.db['info']
