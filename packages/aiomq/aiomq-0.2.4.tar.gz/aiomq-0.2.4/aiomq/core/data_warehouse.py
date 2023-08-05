import asyncio

from aiomq.core.system_signals import WS_DISCONNECTION


class WorkspaceData(object):
    __fields = [
        'pid',
        'alias',
    ]


class TaskData(object):
    __fields = [
        'status',
        'create_date',
        'running_date',
        'during_time',
        'plan_id',
        'worker_id',
        'console',
    ]


class PlanData(object):
    __fields = [
        'worker_id',
        'description',
        'start_date',
        'end_time',
        'is_all_day',
        'repeat',
        'repeat_time'
    ]


class WorkerData(object):
    __fields = [
        'id'
        'mac_address',
        'alias',
        'online',
        'public_ip',
        'private_ip',
        'alive_date',
    ]


class DataWareHouse(object):
    def __init__(self):
        self.connections = {}
        self._listen = {}

    async def disconnection(self, sender_id):
        del self.connections[sender_id]
        WS_DISCONNECTION.send(sender_id)

    async def runtime(self, loop):
        while True:
            await asyncio.sleep(1)

    async def ws_send(self, sender_id, response, cmd='Normal'):
        if isinstance(response, list):
            await self.connections[sender_id].send_json({'data': response, 'key': cmd})
        if isinstance(response, dict):
            await self.connections[sender_id].send_json(response)
        elif isinstance(response, str):
            await self.connections[sender_id].send_str(response)
        elif isinstance(response, (bytes, bytearray)):
            await self.connections[sender_id].send_bytes(response)

    async def broadcast(self, key, response):
        if key in self._listen:
            for sender_id in self._listen[key]:
                if sender_id in self.connections:
                    await self.ws_send(sender_id, response, cmd=key)
                # else:
                    # del self._listen[sender_id]
                    # del self.connections[sender_id]

    def listen(self, key, sender_id):
        if key not in self._listen:
            self._listen[key] = set()
        self._listen[key].update({sender_id})


DATAWAREHOUSE = DataWareHouse()
