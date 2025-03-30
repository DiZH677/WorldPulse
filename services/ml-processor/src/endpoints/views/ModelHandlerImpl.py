from endpoints.models.ml_processor_new_news_post200_response import MlProcessorNewNewsPost200Response
from endpoints.models.ml_processor_new_news_post_request import MlProcessorNewNewsPostRequest
from ..apis.default_api_base import BaseDefaultApi
from endpoints.views.local_model.model import *
import datetime

class DefaultApiImpl(BaseDefaultApi):
    def __init__(self):
        super().__init__()
        self.model = T5Model()

    async def ml_processor_new_news_post(self,
        ml_processor_new_news_post_request: MlProcessorNewNewsPostRequest,
    ) -> MlProcessorNewNewsPost200Response:
        new_text = self.model.summarize([ml_processor_new_news_post_request.text], brief=True)
        return MlProcessorNewNewsPost200Response(id=3, text=new_text, embedding="1,2,3", classes="1,2,3")