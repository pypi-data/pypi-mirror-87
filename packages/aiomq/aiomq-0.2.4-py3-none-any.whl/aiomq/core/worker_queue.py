import asyncio, logging
from uuid import uuid1


class BasicQueue(object):
    """工作队列"""

    def __init__(self):
        self.cron_job = asyncio.Queue()
        self.loop = None
        self.jobs = {}

    async def next(self):
        if self.cron_job.qsize():
            return await self.cron_job.get()
        return None

    async def runtime(self, loop):
        self.loop = loop
        while True:
            await asyncio.sleep(0.1)


WORKERQUEUE = BasicQueue()
