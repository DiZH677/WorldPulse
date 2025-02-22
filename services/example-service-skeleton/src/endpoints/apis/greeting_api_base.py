# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from endpoints.models.get_greeting200_response import GetGreeting200Response


class BaseGreetingApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseGreetingApi.subclasses = BaseGreetingApi.subclasses + (cls,)
    async def get_greeting(
        self,
    ) -> GetGreeting200Response:
        ...
