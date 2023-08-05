import asyncio

import aiohttp
from aiohttp.http_websocket import WSMessage
from aiohttp.web import _run_app as run_app
from aiomq.core import logger
from aiomq.core.data_warehouse import DATAWAREHOUSE
from aiomq.core.receive_queue import receive_package_bytes, receive_package_text
from aiohttp import web


async def basic_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    logger.debug('websocket connection successfully.')
    sender_id = ws.headers.get('Sec-WebSocket-Accept')
    DATAWAREHOUSE.connections[sender_id] = ws
    try:
        async for msg in ws:
            if isinstance(msg, WSMessage):
                if msg.type == aiohttp.WSMsgType.BINARY:
                    await receive_package_bytes(msg.data, sender_id)
                elif msg.type == aiohttp.WSMsgType.TEXT:
                    await receive_package_text(msg.data, sender_id)
                elif msg.type == aiohttp.WSMsgType.PING:
                    await ws.pong()
    finally:
        # 'websocket connection closed'
        await DATAWAREHOUSE.disconnection(sender_id)


def bootstrap_api(host,
                  port,
                  path='/client',
                  ):
    app = web.Application()
    app.add_routes([
        web.get(path, basic_websocket),  # 注册机器设备
    ])
    return run_app(app, host=host, port=port, )

