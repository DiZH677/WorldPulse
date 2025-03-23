from ..models.get_greeting200_response import GetGreeting200Response
from ..apis.default_api_base import BaseDefaultApi

import datetime

class DefaultApiImpl(BaseDefaultApi):
    async def get_greeting(self) -> GetGreeting200Response:
        return GetGreeting200Response(message='hello from news-sender', current_time=datetime.datetime.now(), news_sender_specific_thing='huh')