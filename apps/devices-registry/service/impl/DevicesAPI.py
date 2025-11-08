'''
Devices API implementation
'''

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from service.apis.default_api_base import BaseDefaultApi
from service.repository import db
from service.repository.devices import Device
import service.models.device_info as dto


class DevicesAPI(BaseDefaultApi):

    async def __get_devices_list(self, query):
        return [
            dto.DeviceInfo.from_dict(device.to_dict())
            for device in await db.all(query)
        ]

    async def v1_get_all_devices(self):
        return await self.__get_devices_list(Device.query)

    async def v1_get_devices_of_provider(self, provider):
        query = Device.query.where(Device.provider == provider)
        return await self.__get_devices_list(query)

    async def v1_get_devices_of_provider_and_protocol(self, provider, protocol):
        query = Device.query.where(
            (Device.provider == provider) &
            (Device.protocol == protocol)
        )
        return await self.__get_devices_list(query)

    async def v1_get_device_info(self, provider, protocol, address):
        device = await Device.get({
            'provider': provider,
            'protocol': protocol,
            'address': address
        })

        if not device:
            return JSONResponse(status_code=404, content={
                'message': 'no device with such identifier',
                'code': 404
            })

        return dto.DeviceInfo.from_dict(device.to_dict())

    async def v1_register_device(self, provider, protocol, device):
        await Device.create(provider=provider, protocol=protocol, **device.to_dict())
        return JSONResponse(status_code=201, content={'message': 'device registered'})

    async def v1_unregister_device(self, provider, protocol, address):
        await Device.delete.where(
            Device.provider == provider &
            Device.protocol == protocol &
            Device.address == address
        )

        return JSONResponse(
            status_code=200,
            content={"message": "device deleted"}
        )
