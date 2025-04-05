from endpoints.models.ml_processor_new_news_post200_response import MlProcessorNewNewsPost200Response
from endpoints.models.ml_processor_new_news_post_request import MlProcessorNewNewsPostRequest
from ..apis.default_api_base import BaseDefaultApi
from endpoints.views.local_model.model import T5Model
from endpoints.views.local_model.binarizing import Binarizer
from endpoints.views.local_model.clusterization import Clusterizer
from endpoints.views.local_model.classification import Classificator

class DefaultApiImpl(BaseDefaultApi):
    def __init__(self):
        super().__init__()
        self.model = T5Model()
        self.clusterizer = Clusterizer()
        self.classificator = Classificator()

    async def ml_processor_new_news_post(self,
        ml_processor_new_news_post_request: MlProcessorNewNewsPostRequest,
    ) -> MlProcessorNewNewsPost200Response:
        brief_text = self.model.summarize([ml_processor_new_news_post_request.text], brief=True)
        embedding = self.model.get_embedding(brief_text)
        nearest_cluster = self.clusterizer.find_nearest_cluster(embedding)
        if nearest_cluster:
            brief_text = self.model.summarize([nearest_cluster["content"], brief_text], brief=True)
            embedding = self.model.get_embedding(brief_text)
        categories = self.classificator.predict(embedding)
        return MlProcessorNewNewsPost200Response(id=3, text=brief_text, embedding=str(Binarizer.encode(embedding)), classes=categories)
