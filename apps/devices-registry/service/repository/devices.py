'''
Devices repository
'''

from typing import List

from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError

from service import repository
from service.models.device import Device
from service.models.device_info import DeviceInfo
from service.models.device_update import DeviceUpdate


__select_fields = '''
SELECT
    provider,
    protocol,
    address,
    kind,
    model,
    serialnum,
    name,
    description,
    tags
FROM
    devices
'''

__returning = '''
RETURNING
    provider,
    protocol,
    address,
    kind,
    model,
    serialnum,
    name,
    description,
    tags
'''


class DeviceRecord(Record):
    @property
    def dto(self):
        return DeviceInfo.from_dict(dict(self.items()))


class DeviceException(Exception):
    pass


class DeviceConflict(DeviceException):
    pass


class InvalidDeviceData(DeviceException):
    pass


async def __insert_warmhouse_old_device(device: Device) -> DeviceRecord:
    query = f'''
    INSERT INTO devices(
        provider,
        protocol,
        kind,
        model,
        serialnum,
        name,
        description,
        tags
    )
    VALUES ('warmhouse', 'http', $1, $2, $3, $4, $5, $6)
    {__returning}
    '''

    async with repository.do() as conn:
        device: DeviceRecord = await conn.fetchrow(
            query,
            device.kind,
            device.model,
            device.serialnum,
            device.name,
            device.description,
            device.tags,
            record_class=DeviceRecord
        )
        return device.dto


async def get(provider, protocol, address) -> DeviceInfo:
    query = f'''
    {__select_fields}
    WHERE (provider, protocol, address) = ($1, $2, $3)
    '''
    async with repository.do() as conn:
        record: DeviceRecord = await conn.fetchrow(
            query,
            provider,
            protocol,
            address,
            record_class=DeviceRecord
        )
        if not record:
            return

        return record.dto


async def select(provider=None, protocol=None) -> List[DeviceInfo]:
    query = f'''
    {__select_fields}
    WHERE
    '''

    args = []
    clauses = ['TRUE']
    if provider is not None:
        args.append(provider)
        clauses.append(f'provider = ${len(args)}')
    if protocol is not None:
        args.append(protocol)
        clauses.append(f'protocol = ${len(args)}')
    query += ' AND '.join(clauses)

    async with repository.do() as conn:
        return [
            record.dto
            for record in await conn.fetch(
                query,
                *args,
                record_class=DeviceRecord
            )
        ]


async def new(provider, protocol, device: Device) -> DeviceInfo:
    if provider == 'warmhouse' and protocol == 'http':
        return await __insert_warmhouse_old_device(device)
    if device.address is None:
        raise InvalidDeviceData("address should be presented")

    query = f'''
    INSERT INTO devices(
        provider,
        protocol,
        address,
        kind,
        model,
        serialnum,
        name,
        description,
        tags
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    {__returning}
    '''

    async with repository.do() as conn:
        try:
            created_device: DeviceRecord = await conn.fetchrow(
                query,
                provider,
                protocol,
                device.address,
                device.kind,
                device.model,
                device.serialnum,
                device.name,
                device.description,
                device.tags,
                record_class=DeviceRecord
            )

            return created_device.dto
        except UniqueViolationError:
            raise DeviceConflict()


async def update(provider, protocol, address, device: DeviceUpdate) -> DeviceInfo:
    query = f'''
    UPDATE devices
    SET
        name = $4,
        description = $5,
        tags = $6
    WHERE (provider, protocol, address) =  ($1, $2, $3)
    {__returning}
    '''

    async with repository.do() as conn:
        updated_device: DeviceRecord = await conn.fetchrow(
            query,
            provider,
            protocol,
            address,
            device.name,
            device.description,
            device.tags,
            record_class=DeviceRecord
        )
        if not updated_device:
            return

        return updated_device.dto


async def delete(provider, protocol, address):
    async with repository.do() as conn:
        deleted: DeviceRecord = await conn.fetchrow(
            f'''
            DELETE FROM
                devices
            WHERE
                provider = $1 AND
                protocol = $2 AND
                address = $3
            {__returning}
            ''',
            provider,
            protocol,
            address,
            record_class=DeviceRecord
        )

        if not deleted:
            return False

        return True
