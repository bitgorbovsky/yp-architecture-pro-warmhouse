# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from service.models.device import Device
from service.models.device_info import DeviceInfo
from service.models.device_update import DeviceUpdate
from service.models.error_message import ErrorMessage
from service.models.success_message import SuccessMessage


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def v1_get_all_devices(
        self,
    ) -> List[DeviceInfo]:
        """Получение полного списка приборов пользователя по всем поддерживаемым провайдерам и протоколам. """
        ...


    async def v1_get_devices_of_provider(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
    ) -> List[DeviceInfo]:
        """Получение полного списка приборов пользователя по указанному провайдеру и поддерживаемым им протоколам. """
        ...


    async def v1_get_devices_of_provider_and_protocol(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
    ) -> List[DeviceInfo]:
        """Получение полного списка приборов пользователя по указанным провайдеру и протоколу. """
        ...


    async def v1_register_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        device: Optional[Device],
    ) -> DeviceInfo:
        """Регистрация прибора в системе для указанного провайдера и протокола. """
        ...


    async def v1_get_device_info(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
    ) -> DeviceInfo:
        """Получение сведений по прибору, занесеённых в системе и привязанных к пользователю. """
        ...


    async def v1_update_device_info(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
        device_update: Optional[DeviceUpdate],
    ) -> DeviceInfo:
        """Изменение сведений по прибору, занесеённых в системе и привязанных к пользователю. """
        ...


    async def v1_unregister_device(
        self,
        provider: Annotated[StrictStr, Field(description="Идентификатор провайдера приборов. ")],
        protocol: Annotated[StrictStr, Field(description="Идентификатор протокола приборов. ")],
        address: Annotated[StrictStr, Field(description="Адрес прибора в части провайдера, обслуживающей заданный протокол. ")],
    ) -> SuccessMessage:
        """Прибор удаляется из списка приборов пользователя. """
        ...
