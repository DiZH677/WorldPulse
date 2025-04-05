from sentence_transformers.util import cos_sim
from endpoints.views.MongoContext import MongoDBManager
from endpoints.views.local_model.binarizing import Binarizer


class Clusterizer:
    def __init__(self):
        self.mongo = MongoDBManager()

    def custom_distance(self, x, y):
        return 1 - cos_sim(x, y)[0][0].item()

    def find_nearest_cluster(self, embedding):
        all_news = self.mongo.get_all_news()
        nearest_cluster = None
        min_distance = 10e6
        for news in all_news:
            distance = self.custom_distance(
                Binarizer.decode(news["embedding"]), embedding)
            if min_distance > distance:
                min_distance = distance
                nearest_cluster = news
        if min_distance <= 0.1:
            return nearest_cluster
        return None
        
