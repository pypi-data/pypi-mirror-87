import sys
import asyncio

from aiomq.core.clock import GLOBAL_CLOCK
from aiomq.core.websocket import bootstrap_api
from aiomq.core.push_queue import PUSH_QUEUE
from aiomq.core.receive_queue import RECEIVE_QUEUE
from aiomq.core.data_warehouse import DATAWAREHOUSE


class AioMQ(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    @classmethod
    def receive_package(cls, func):
        RECEIVE_QUEUE.receive_package = func

    @classmethod
    def event(cls, route_name):
        def warps(func):
            RECEIVE_QUEUE.listen[route_name] = func

        return warps

    def get_task(self):
        return asyncio.gather(
            asyncio.ensure_future(GLOBAL_CLOCK.runtime(self.loop)),
            asyncio.ensure_future(PUSH_QUEUE.runtime(self.loop)),
            asyncio.ensure_future(RECEIVE_QUEUE.runtime(self.loop)),
            asyncio.ensure_future(DATAWAREHOUSE.runtime(self.loop)),
            asyncio.ensure_future(bootstrap_api(host='127.0.0.1', port=8080)),
            # asyncio.ensure_future(init_db()),
        )


if __name__ == '__main__':
    print(sys.argv)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AioMQ().get_task())
