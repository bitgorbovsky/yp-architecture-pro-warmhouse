# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from service.apis.default_api_base import BaseDefaultApi
import service.impl

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

from service.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Optional
from typing_extensions import Annotated
from service.models.device_state import DeviceState
from service.models.error_message import ErrorMessage
from service.models.success_message import SuccessMessage


router = APIRouter()

ns_pkg = service.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/control/{provider}/{protocol}/{address}",
    responses={
        200: {"model": DeviceState, "description": "Состояние прибора."},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
    },
    tags=["default"],
    summary="Получение состояния прибора.",
    response_model_by_alias=True,
)
async def v1_inspect_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
) -> DeviceState:
    """Получение полного состояния прибора."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_inspect_device(provider, protocol, address)


@router.post(
    "/v1/control/{provider}/{protocol}/{address}",
    responses={
        201: {"model": DeviceState, "description": "Состояние прибора."},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
    },
    tags=["default"],
    summary="Запуск управления прибором",
    response_model_by_alias=True,
)
async def v1_connect_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
) -> DeviceState:
    """Создаёт сеанс управления прибором и запрашивает его начальное состояние. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_connect_device(provider, protocol, address)


@router.delete(
    "/v1/control/{provider}/{protocol}/{address}",
    responses={
        200: {"model": SuccessMessage, "description": "Ответ на любую успешную операцию. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
    },
    tags=["default"],
    summary="Останов управления прибором",
    response_model_by_alias=True,
)
async def v1_disconnect_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
) -> SuccessMessage:
    """Останавливает сеанс управления прибором и удаляет его состояние из системы. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_disconnect_device(provider, protocol, address)


@router.patch(
    "/v1/control/{provider}/{protocol}/{address}",
    responses={
        202: {"model": SuccessMessage, "description": "Ответ на любую успешную операцию. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        400: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
        403: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
        404: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
        422: {"model": ErrorMessage, "description": "Ответ на некорректную операцию. "},
    },
    tags=["default"],
    summary="Установка целевого состояния прибора.",
    response_model_by_alias=True,
)
async def v1_run_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
    device_state: Optional[DeviceState] = Body(None, description=""),
) -> SuccessMessage:
    """Установка целевого состояния прибора."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_run_device(provider, protocol, address, device_state)
