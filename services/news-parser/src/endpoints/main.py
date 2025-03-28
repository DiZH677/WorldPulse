# coding: utf-8

"""
    news-parser

    Парсер новостей из тг каналов

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from endpoints.apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="news-parser",
    description="Парсер новостей из тг каналов",
    version="1.0.0",
)

app.include_router(DefaultApiRouter)
