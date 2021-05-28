from pymongo import MongoClient


class Mongo:
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)
        self.database = self.client.test  # use test as default

    def getClient(self):
        return self.client

    def getDatabase(self, database='test', username='user', password='123456789'):
        self.database.authenticate(username, password)
        self.database = eval('self.client.' + database)
        return self.database

    def changeHost(self, host):
        self.host = host
        self.client = MongoClient(self.host, self.port)

    def __del__(self):
        self.client.close()


M = Mongo()
