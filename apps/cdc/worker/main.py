'''
CDC worker
'''

import os
import sys
import json
import time
import logging


import redis
import requests
from redis.exceptions import ResponseError


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)


def wait_for_stream(client, stream_name):
    groupname = '%s-group' % stream_name
    try:
        client.xinfo_groups(stream_name)
        logger.info("consumer group exists, subscribe")
        return
    except ResponseError as e:
        if e.args[0] != 'no such key':
            return

    while True:
        try:
            logger.info("create consumer group")
            client.xgroup_create(
                name=stream_name,
                groupname=groupname,
                id=0
            )
            break
        except ResponseError as e:
            errmsg, *_ = e.args
            if errmsg.startswith('The XGROUP subcommand requires the key to exist'):
                logger.warn("no stream, waiting...")
                time.sleep(1)
                continue


def main():
    logger.info("start")
    registry_url = os.getenv('DEVICES_REGISTRY_URL')
    client = redis.Redis(
        host=os.getenv('CDC_BUS_HOST'),
        port=os.getenv('CDC_BUS_PORT'),
        db=int(os.getenv('CDC_BUS_DB'))
    )

    stream_name = os.getenv("CDC_BUS_STREAM")
    wait_for_stream(client, stream_name)
    groupname = '%s-group' % stream_name
    while True:
        result = client.xreadgroup(
            groupname=groupname,
            consumername='cdc-bus-processor',
            streams={stream_name: '>'},
            count=100,
            block=1000
        )
        if result is None or not result:
            continue
        stream, *_ = result
        for msgid, message in stream[1]:
            key = json.loads(list(message.keys())[0])
            value = json.loads(list(message.values())[0])
            record = value['payload']
            if record['__op'] == 'c':
                response = requests.post(
                    '%s/v1/devices/warmhouse/http' % registry_url,
                    json={
                        'kind': 'temperature' \
                            if record['type'] == 'temperature' \
                            else 'thermostat',
                        'model': 'WarmhouseTempSensor-1',
                        'serialnum': 'WHTS1-%s' % record['id'],
                        'address': str(record['id']),
                        'name': record['name'],
                        'tags': [
                            record['location']
                        ]
                    }
                )
                logger.info('response from service: %s', json.dumps(response.json()))
            client.xack(stream[0], groupname, msgid)

    client.close()

if __name__ == '__main__':
    main()
