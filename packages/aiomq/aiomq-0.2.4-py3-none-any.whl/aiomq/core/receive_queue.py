import asyncio, logging
from uuid import uuid1
from aiomq.core.data_warehouse import DATAWAREHOUSE
from aiomq.core import logger
from aiomq import exception
from aiomq.exception import AioMQCloseWebsocket


class ReceiveQueue(object):
    """工作队列"""

    def __init__(self):
        self.cron_job = asyncio.Queue()
        self.loop = None
        self.listen = {}
        self.jobs = {}

    @classmethod
    async def receive_package(cls, msg):
        return 'debug', msg, msg

    async def runtime(self, loop):
        self.loop = loop
        while True:
            payload = await self.cron_job.get()
            if payload.name in self.listen:
                try:
                    response = await self.listen[payload.name](payload)
                    if response is not None:
                        await DATAWAREHOUSE.ws_send(payload.sender_id, response, cmd=payload.name)
                except AioMQCloseWebsocket:
                    await payload.sender.close()


RECEIVE_QUEUE = ReceiveQueue()


class Payload(object):
    def __init__(self, name, msg_id, data, sender_id):
        self.name = name
        self.msg_id = msg_id
        self.data = data
        self.sender_id = sender_id

    def __str__(self):
        return f"name: {self.name.upper()}, data: {repr(self.data)[:200]}"


async def receive_package_bytes(msg_bytes, sender_id):
    await receive_package_text(msg_bytes.encode(), sender_id)


async def receive_package_text(msg_text, sender_id):
    logger.debug(f'receive package: {msg_text}.')
    try:
        route_name, data, msg_id = await RECEIVE_QUEUE.receive_package(msg_text)
        payload = Payload(route_name, msg_id, data, sender_id)
        logger.info(f'revice payload: {payload}')
        await RECEIVE_QUEUE.cron_job.put(payload)
        # await DATAWAREHOUSE.ws_send(sender_id, {'received': True, 'msg_id': msg_id})
    except exception.AioMQReceiveFormatError:
        await DATAWAREHOUSE.ws_send(sender_id, {'received': False, 'content': msg_text, 'msg_id': None})
