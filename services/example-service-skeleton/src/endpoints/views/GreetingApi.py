from ..models.get_greeting200_response import GetGreeting200Response
from ..apis.greeting_api_base import BaseGreetingApi

import datetime

class GreetinApiImpl(BaseGreetingApi):
    async def get_greeting(self) -> GetGreeting200Response:
        return GetGreeting200Response(message='Hello World!', currentTime=datetime.datetime.now())