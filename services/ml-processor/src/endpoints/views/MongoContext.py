from urllib.parse import quote_plus as quote
from typing import Dict, List
import pymongo
import os


class MongoDBManager:
    def __init__(self):
        self._url = "mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}".format(
            user=quote("wpdev"),
            pw=quote(os.getenv("MONGO_PASSWORD")),
            hosts=",".join([os.getenv("MONGO_HOST")]),
            rs="rs01",
            auth_src="worldpulse",
        )
    
    def _get_connection(self):
        return pymongo.MongoClient(
            self._url, tls=True, tlsCAFile=".mongodb/root.crt"
        )

    def add_news_entry(self, 
                      content: str, 
                      categories: List[int],
                      database_name: str = "worldpulse",
                      collection_name: str = "news") -> str:
        doc = self.prepare_news_entry(content, categories)
        
        with self._get_connection() as client:
            db = client[database_name]
            result = db[collection_name].insert_one(doc)
            return str(result.inserted_id)

    def get_all_news(self,
                    database_name: str = "worldpulse",
                    collection_name: str = "news") -> List[Dict]:
        with self._get_connection() as client:
            db = client[database_name]
            collection = db[collection_name]
            
            return [{
                "_id": doc["_id"],
                "content": doc["content"],
                "categories": doc.get("categories", []),
                "embedding": doc["embedding"]
            } for doc in collection.find()]
