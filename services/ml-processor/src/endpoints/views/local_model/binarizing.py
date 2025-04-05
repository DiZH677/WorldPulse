from pickle import loads, dumps
from bson.binary import Binary


class Binarizer:
    
    @staticmethod
    def encode(data):
        return Binary(dumps(data, protocol=3))
    
    @staticmethod
    def decode(data):
        return loads(data)
