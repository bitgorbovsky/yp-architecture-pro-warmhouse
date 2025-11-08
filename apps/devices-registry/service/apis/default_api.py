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
from typing import List, Optional
from typing_extensions import Annotated
from service.models.device import Device
from service.models.device_info import DeviceInfo
from service.models.error_message import ErrorMessage
from service.models.success_message import SuccessMessage


router = APIRouter()

ns_pkg = service.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/devices",
    responses={
        200: {"model": List[DeviceInfo], "description": "Список приборов. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
    },
    tags=["default"],
    summary="Получение списка приборов.",
    response_model_by_alias=True,
)
async def v1_get_all_devices(
) -> List[DeviceInfo]:
    """Получение полного списка приборов пользователя по всем поддерживаемым провайдерам и протоколам. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_get_all_devices()


@router.get(
    "/v1/devices/{provider}",
    responses={
        200: {"model": List[DeviceInfo], "description": "Список приборов. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Получение списка приборов.",
    response_model_by_alias=True,
)
async def v1_get_devices_of_provider(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
) -> List[DeviceInfo]:
    """Получение полного списка приборов пользователя по указанному провайдеру и поддерживаемым им протоколам. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_get_devices_of_provider(provider)


@router.get(
    "/v1/devices/{provider}/{protocol}",
    responses={
        200: {"model": List[DeviceInfo], "description": "Список приборов. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Получение списка приборов.",
    response_model_by_alias=True,
)
async def v1_get_devices_of_provider_and_protocol(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
) -> List[DeviceInfo]:
    """Получение полного списка приборов пользователя по указанным провайдеру и протоколу. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_get_devices_of_provider_and_protocol(provider, protocol)


@router.post(
    "/v1/devices/{provider}/{protocol}",
    responses={
        201: {"model": DeviceInfo, "description": "Данные по прибору пользователя. "},
        400: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Регистрация прибора в системе и его привязка к пользователю.",
    response_model_by_alias=True,
)
async def v1_register_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    device: Optional[Device] = Body(None, description=""),
) -> DeviceInfo:
    """Регистрация прибора в системе для указанного провайдера и протокола. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_register_device(provider, protocol, device)


@router.get(
    "/v1/devices/{provider}/{protocol}/{address}",
    responses={
        200: {"model": DeviceInfo, "description": "Данные по прибору пользователя. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Получение информации по прибору.",
    response_model_by_alias=True,
)
async def v1_get_device_info(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
) -> DeviceInfo:
    """Получение сведений по прибору, занесеённых в системе и привязанных к пользователю. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_get_device_info(provider, protocol, address)


@router.put(
    "/v1/devices/{provider}/{protocol}/{address}",
    responses={
        200: {"model": DeviceInfo, "description": "Данные по прибору пользователя. "},
        400: {"model": ErrorMessage, "description": "Валидация входных данных вернула ошибку."},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Изменение данных по прибору.",
    response_model_by_alias=True,
)
async def v1_update_device_info(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
    device: Optional[Device] = Body(None, description=""),
) -> DeviceInfo:
    """Изменение сведений по прибору, занесеённых в системе и привязанных к пользователю. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_update_device_info(provider, protocol, address, device)


@router.delete(
    "/v1/devices/{provider}/{protocol}/{address}",
    responses={
        200: {"model": SuccessMessage, "description": "Ответ на любую успешную операцию. "},
        401: {"model": ErrorMessage, "description": "Не был предоставлен токен авторизации, сервер не может обработать запрос. "},
        404: {"model": ErrorMessage, "description": "Указан не поддерживаемый провайдер или протокол, или прибор не найден по указанному адресу. "},
    },
    tags=["default"],
    summary="Отвязка прибора от пользователя и его удаление.",
    response_model_by_alias=True,
)
async def v1_unregister_device(
    provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")] = Path(..., description="Идентификатор провайдера приборов. "),
    protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")] = Path(..., description="Идентификатор протокола приборов. "),
    address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")] = Path(..., description="Адрес прибора в части провайдера, обслуживающей заданный протокол. "),
) -> SuccessMessage:
    """Прибор удаляется из списка приборов пользователя. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().v1_unregister_device(provider, protocol, address)
