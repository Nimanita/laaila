from pymongo import MongoClient
from django.conf import settings


class MongoConnection(object):
    def __init__(self):
        DATABASES = settings.DATABASES
        
        self.client = MongoClient(host=[DATABASES['CONTRACTS']['HOST']],
                                  username=DATABASES['CONTRACTS']['USERNAME'],
                                  password=DATABASES['CONTRACTS']['PASSWORD']
                                ,
                                 connect=False)
        self.db = self.client[DATABASES['CONTRACTS']['DATABASE']]

    def get_collection(self, name):
        self.collection = self.db[name]