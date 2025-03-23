from ..models.get_greeting200_response import GetGreeting200Response
from ..apis.default_api_base import BaseDefaultApi

import datetime

import ml_processor_client
import news_sender_client
import telegram_bot_client

def make_client(lib, host):
    api_client = lib.ApiClient(lib.Configuration(host=host))
    return lib.DefaultApi(api_client)

class DefaultApiImpl(BaseDefaultApi):
    async def get_greeting(self) -> GetGreeting200Response:
        ml_client = make_client(ml_processor_client, 'http://ml-processor:8080')
        ns_client = make_client(news_sender_client, 'http://news-sender:8080')
        tg_client = make_client(telegram_bot_client, 'http://telegram-bot:8080')

        ml_response = ml_client.get_greeting()
        ns_response = ns_client.get_greeting()
        tg_client_response = tg_client.get_greeting()

        return GetGreeting200Response(additional_properties={'ml': ml_response, 'ns': ns_response, 'tg': tg_client_response})