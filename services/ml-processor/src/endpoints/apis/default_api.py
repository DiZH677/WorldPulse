# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from endpoints.apis.default_api_base import BaseDefaultApi
import endpoints

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from endpoints.models.extra_models import TokenModel  # noqa: F401
from endpoints.models.ml_processor_new_news_post200_response import MlProcessorNewNewsPost200Response
from endpoints.models.ml_processor_new_news_post_request import MlProcessorNewNewsPostRequest


router = APIRouter()

ns_pkg = endpoints
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/ml-processor/new_news",
    responses={
        200: {"model": MlProcessorNewNewsPost200Response, "description": "Успешный возврат записи в бд"},
    },
    tags=["default"],
    summary="Возвращает результат работы моделей",
    response_model_by_alias=True,
)
async def ml_processor_new_news_post(
    ml_processor_new_news_post_request: MlProcessorNewNewsPostRequest = Body(None, description=""),
) -> MlProcessorNewNewsPost200Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().ml_processor_new_news_post(ml_processor_new_news_post_request)
