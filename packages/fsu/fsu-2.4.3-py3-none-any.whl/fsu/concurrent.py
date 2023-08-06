from collections import namedtuple
from contextlib import asynccontextmanager
from asyncio import sleep
from os import urandom

RedisLock = namedtuple("RedisLock", ["lock"])

def make_redis_lock(redis):
    @asynccontextmanager
    async def lock(key, timeout = 60):
        v = urandom(20)

        accuired = False

        while not accuired:
            accuired = await redis.set(key, v, expire=timeout, exist="SET_IF_NOT_EXIST")

            if not accuired:
                await sleep(1)

        try:
            yield
        finally:
            await redis.eval("""
                if redis.call("get", KEYS[1]) == ARGV[1]
                then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
            """, [key], [v])

    redis_lock = RedisLock(
        lock = lock,
    )

    return redis_lock
