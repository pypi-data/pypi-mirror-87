from functools import wraps
from msgpack import packb, unpackb

def make_redcache(redis, prefix="redcache"):
    def cache(period, hash_func):
        def f(wrapped):
            @wraps(wrapped)
            async def g(*args, **kwargs):
                key = f"{prefix}:{f.__module__}.{f.__qualname__}:{hash_func(*args, **kwargs)}"

                # NOTE there is a get-set issue but it donesn't matter.....
                try:
                    v = await redis.get(key)
                except:
                    v = None

                if v is None:
                    v = await wrapped(*args, **kwargs)
                    try:
                        await redis.set(key, packb(v), expire=period, exist="SET_IF_NOT_EXIST")
                    except:
                        pass
                else:
                    v = unpackb(v)

                return v

            return g

        return f

    return cache
