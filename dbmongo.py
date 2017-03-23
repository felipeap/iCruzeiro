from bson import json_util
from datetime import date, datetime
__author__ = 'felipepereira'

from pymongo import MongoClient
import json
from pprint import pprint

class Database:
    conn = None
    def __init__(self):
        if self.conn is None:
            self.conn = MongoClient('localhost:27017')
            self.db = self.conn["MeusJogos"]

    def add(self, data, col):
        self.__init__()
        # r_json = json.dumps(data.__dict__, default=json_util.default)
        r_json = json.dumps(data.__dict__,cls=DatetimeEncoder)
        r_json = json.loads(r_json, object_hook=json_util.object_hook)
        collection = self.db[col]
        collection.insert(r_json)

    def getdata(self, query, sortby, collection):
        self.__init__()
        self.pesquisa = self.db[collection]
        if sortby != 0:
            return self.pesquisa.find(query).sort(sortby)
        else:
            return self.pesquisa.find(query)

    def updatedata(self, query, data, collection):
        self.__init__()
        self.pesquisa = self.db[collection]
        return self.pesquisa.replace_one(query, data)

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)