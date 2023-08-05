import asyncio
from time import time


class GlobalClock:
    """定时任务"""

    def __init__(self):
        self.cron_job = {}
        self.loop = None
        self.last_time = time()

    async def runtime(self, loop):
        while True:
            for job in self.cron_job.values():
                if job.get('future'):
                    if job['future'].done():
                        job['last_time'] = time()
                        job['future'] = None
                elif job['last_time'] + job['every'] <= time():
                    job['future'] = asyncio.create_task(
                        job['callback']()
                    )
            await asyncio.sleep(1)

    def clock(self, name, every, desc=''):
        def wraps(func):
            self.cron_job[name] = {
                'name': name,
                'desc': desc,
                'every': every,
                'callback': func,
                'last_time': time(),
                'future': None
            }
        return wraps


GLOBAL_CLOCK = GlobalClock()
