import asyncio
import aiohttp
import time


async def async_post(url, data, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as res:
                return res.text()


async def async_get(url, params, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                return res.text()


async def run():
    # TODO: 修改 并发数、网址|api列表、传参列表
    sem = asyncio.Semaphore(90)  # 限制并发量为
    urls = ['', '']
    pdatas = [{}, {}]
    tasks = [async_post(url, pdata, sem) for url, pdata in zip(urls, pdatas)]
    await asyncio.wait(tasks)

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
end = time.time()

print(f'time consumed : {end-start}')
# TODO：最后数据存储和异步数据库存储（aiomysql）（可参考lianjia2）
