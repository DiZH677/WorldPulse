from ..models.get_greeting200_response import GetGreeting200Response
from ..apis.default_api_base import BaseDefaultApi

import datetime

class DefaultApiImpl(BaseDefaultApi):
    async def get_greeting(self) -> GetGreeting200Response:
        return GetGreeting200Response(message='hello from ml', current_time=datetime.datetime.now(), ml_specific_thing=228)