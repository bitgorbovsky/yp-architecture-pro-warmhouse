# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Optional
from typing_extensions import Annotated
from service.models.device_state import DeviceState
from service.models.error_message import ErrorMessage
from service.models.success_message import SuccessMessage


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def v1_inspect_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
    ) -> DeviceState:
        """Получение полного состояния прибора."""
        ...


    async def v1_connect_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
    ) -> DeviceState:
        """Создаёт сеанс управления прибором и запрашивает его начальное состояние. """
        ...


    async def v1_disconnect_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
    ) -> SuccessMessage:
        """Останавливает сеанс управления прибором и удаляет его состояние из системы. """
        ...


    async def v1_run_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
        device_state: Optional[DeviceState],
    ) -> SuccessMessage:
        """Установка целевого состояния прибора."""
        ...
