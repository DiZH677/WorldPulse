# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from endpoints.models.ml_processor_new_news_post200_response import MlProcessorNewNewsPost200Response
from endpoints.models.ml_processor_new_news_post_request import MlProcessorNewNewsPostRequest


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def ml_processor_new_news_post(
        self,
        ml_processor_new_news_post_request: MlProcessorNewNewsPostRequest,
    ) -> MlProcessorNewNewsPost200Response:
        ...
