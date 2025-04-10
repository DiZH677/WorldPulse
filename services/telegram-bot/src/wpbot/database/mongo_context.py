import os
from urllib.parse import quote_plus as quote

import pymongo


class MongoDBConnectionManager:
    def __init__(self, mongo_password, mongo_host):
        self.__url = "mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}".format(
            user=quote("wpdev"),
            pw=quote(mongo_password),
            hosts=",".join([mongo_host]),
            rs="rs01",
            auth_src="worldpulse",
        )
        self.__connection = pymongo.MongoClient(
            self.__url, tls=True, tlsCAFile=f".mongodb/root.crt"
        )

    def close(self):
        self.__connection.close()

    @property
    def db(self):
        return self.__connection["worldpulse"]
