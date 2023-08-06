import aiohttp
import time

async def req_async(url: str):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as resp:
            return await resp.json()

async def time_took(st: float) -> float:
    time_taken = (time.time_ns() - st) / 1000 # nanos -> micros
    time_str = (f'{time_taken:.2f}μs' if time_taken < 1000
        else f'{time_taken / 1000:.2f}ms')

    return time_str