from ..models.get_greeting200_response import GetGreeting200Response, GetGreeting200ResponseTgBotThing
from ..apis.default_api_base import BaseDefaultApi

import datetime

class DefaultApiImpl(BaseDefaultApi):
    async def get_greeting(self) -> GetGreeting200Response:
        return GetGreeting200Response(message='hello from telegramm', current_time=datetime.datetime.now(), tg_bot_thing=GetGreeting200ResponseTgBotThing(test_prop='sheesh'))
