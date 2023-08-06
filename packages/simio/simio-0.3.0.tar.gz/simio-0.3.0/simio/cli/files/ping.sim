from asyncio import sleep

from aiohttp import web


async def ping_worker(app: web.Application, sleep_time: int):
    while True:
        app.logger.info('Background worker works!')
        await sleep(sleep_time)
