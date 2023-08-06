from typing import Awaitable, Any, Union, TypeVar, List, Tuple, Optional, cast
from asyncio import create_task, sleep, Semaphore, Future
from collections import namedtuple
from logging import getLogger, Logger
from datetime import datetime
from itertools import chain
from time import time
from uuid import uuid4
from enum import Enum
import inspect
import re

from aioredis import Redis
from msgpack import packb, unpackb

T = TypeVar("T")

class Stage(Enum):
    acked    = "acked"
    handling = "handling"

STAGE_MAXLEN = max(len(l.value) for l in Stage)

Dispatcher = namedtuple("Dispatcher", ["listen", "unlisten", "handler", "callback_handler", "resolve", "search", "cancel", "init"])

logger : Logger = getLogger("fsu.mq")

async def extract_co(co_or_v : Union[Awaitable[T], T]) -> T:
    if inspect.isawaitable(co_or_v):
        return await cast(Awaitable[T], co_or_v)
    else:
        return cast(T, co_or_v)

RE_WORD = re.compile(r"\w+")
def shorten_kind(kind: str) -> str:
    for m in reversed(list(RE_WORD.finditer(kind))[:-1]):
        w     = m.group(0)
        start = m.start(0)
        end   = m.end(0)

        s = "_".join(sw[0] for sw in w.split("_"))
        kind = kind[:start] + s + kind[end:]

    return kind

def expand_args(args : List[Any], kwargs : List[Tuple[str, Any]]) -> str:
    arg_reprs   = (repr(v) for v in args)
    kwarg_reprs = (f"{k}={repr(v)}" for k, v in kwargs)

    return ", ".join(chain(arg_reprs, kwarg_reprs))

def repr_task(label : Stage, task) -> str:
    full_label = label.value.ljust(STAGE_MAXLEN).capitalize()

    if task["eta"] is None:
        eta = int(time())
    else:
        eta = task["eta"]

    eta_str = datetime.fromtimestamp(eta).strftime('%m-%d %H:%M:%S')
    id_     = task["id"]
    kind    = task["kind"]
    args    = task["args"]
    kwargs  = task["kwargs"]

    if task["has_callback"]:
        callback_suffix = f"({task['value']})"
    else:
        callback_suffix = ""

    return f"{full_label} {eta_str} {id_} {shorten_kind(kind)}({expand_args(args, kwargs)}){callback_suffix}"

def make_dispatcher(name, redis : Redis, max_ttl = 60, max_size = 100, on_exception = None, repr_task = repr_task):
    listener_task = None
    handlers      = {}
    stopped       = False
    semaphore     = Semaphore(value=max_size)
    lua_scripts   = {}
    lua_actions   = {} # type: ignore

    dt_zset_queued = f"{name}:queued"
    dt_hash_task   = f"{name}:task"
    dt_hash_proc   = f"{name}:processing"
    dt_set_pend    = f"{name}:pending"

    async def handle_exception(e : Exception) -> Optional[T]:
        if on_exception is not None:
            return await extract_co(on_exception(e))
        else:
            return None

    def lua_action(script):
        def wrapper(f):
            action_name = f.__name__

            lua_scripts[action_name] = script
            lua_actions[action_name] = Future()

            async def g(*args, **kwargs):
                sha = await lua_actions[action_name]
                return await f(sha, *args, **kwargs)

            return g

        return wrapper

    async def init():
        for action_name, script in lua_scripts.items():
            sha = await redis.script_load(script)

            lua_actions[action_name].set_result(sha)

    # redis actions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @lua_action("""
        local dt_zset_queued = KEYS[1]
        local dt_hash_task   = KEYS[2]

        local eta     = tonumber(ARGV[1])
        local task_id = ARGV[2]
        local taskb   = ARGV[3]

        redis.call("zadd", dt_zset_queued, eta    , task_id)
        redis.call("hset", dt_hash_task  , task_id, taskb)
    """)
    async def enqueue(sha, task) -> None:
        await redis.evalsha(sha, [dt_zset_queued, dt_hash_task], [task["eta"], task["id"], packb(task)])

    @lua_action("""
        local dt_zset_queued = KEYS[1]
        local dt_hash_task   = KEYS[2]
        local dt_hash_proc   = KEYS[3]
        local now            = tonumber(ARGV[1])

        local ret = redis.call("zpopmin", dt_zset_queued)

        if #ret == 0 then
            return nil
        end

        local task_id = ret[1]

        redis.call("hset", dt_hash_proc, task_id, now)

        return redis.call("hget", dt_hash_task, task_id)
    """)
    async def dequeue(sha):
        taskb = await redis.evalsha(sha, [dt_zset_queued, dt_hash_task, dt_hash_proc], [int(time())])
        task  = taskb and unpackb(taskb)

        return task

    @lua_action("""
        local dt_zset_queued = KEYS[1]
        local dt_hash_task   = KEYS[2]
        local dt_hash_proc   = KEYS[3]
        local task_id        = ARGV[1]

        local taskb = redis.call("hget", dt_hash_task, task_id)
        local task  = cmsgpack.unpack(taskb)

        redis.call("hdel", dt_hash_proc  , task_id)
        redis.call("zadd", dt_zset_queued, task.eta, task_id)
    """)
    async def re_enqueue(sha, task_id):
        await redis.evalsha(sha, [dt_zset_queued, dt_hash_task, dt_hash_proc], [task_id])

    @lua_action("""
        local dt_hash_task = KEYS[1]
        local dt_set_pend  = KEYS[2]
        local task_id      = ARGV[1]
        local taskb        = ARGV[2]

        redis.call("sadd", dt_set_pend , task_id)
        redis.call("hset", dt_hash_task, task_id , taskb)
    """)
    async def wait_for_resolve(sha, task) -> None:
        await redis.evalsha(sha, [dt_hash_task, dt_set_pend], [task["id"], packb(task)])

    @lua_action("""
        local dt_zset_queued = KEYS[1]
        local dt_hash_task   = KEYS[2]
        local dt_set_pend    = KEYS[3]
        local task_id        = ARGV[1]
        local now            = tonumber(ARGV[2])
        local value          = cmsgpack.unpack(ARGV[3])

        local is_pending = redis.call("sismember", dt_set_pend, task_id)

        if not is_pending then
            return
        end

        local taskb = redis.call("hget", dt_hash_task, task_id)
        local task  = cmsgpack.unpack(taskb)

        task.value = value
        task.eta   = now

        taskb = cmsgpack.pack(task)

        redis.call("hset", dt_hash_task  , task_id , taskb)
        redis.call("srem", dt_set_pend   , task_id)
        redis.call("zadd", dt_zset_queued, now     , task_id)
    """)
    async def resolve(sha, task_id, value = None) -> None:
        await redis.evalsha(sha, [dt_zset_queued, dt_hash_task, dt_set_pend], [task_id, int(time()), packb(value)])

    @lua_action("""
        local dt_hash_task = KEYS[1]
        local dt_hash_proc = KEYS[2]
        local task_id      = ARGV[1]

        redis.call("hdel", dt_hash_proc, task_id)
        redis.call("hdel", dt_hash_task, task_id)
    """)
    async def ack(sha, task_id) -> None:
        await redis.evalsha(sha, [dt_hash_task, dt_hash_proc], [task_id])

    @lua_action("""
        local dt_zset_queued = KEYS[1]
        local dt_hash_task   = KEYS[2]
        local dt_hash_proc   = KEYS[3]
        local dt_set_pend    = KEYS[4]
        local task_id        = ARGV[1]

        redis.call("hdel", dt_hash_proc  , task_id)
        redis.call("hdel", dt_hash_task  , task_id)
        redis.call("srem", dt_set_pend   , task_id)
        redis.call("zrem", dt_zset_queued, task_id)
    """)
    async def cancel(sha, task_id) -> None:
        await redis.evalsha(sha, [dt_zset_queued, dt_hash_task, dt_hash_proc, dt_set_pend], [task_id])

    # decorators >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def handler(kind = None):
        def wrapper(f):
            kind_ = kind or f"{f.__module__}.{f.__qualname__}"

            handlers[kind_] = f

            async def call_at(eta = None, args = [], kwargs = {}):
                id_ = str(uuid4())

                if eta is None:
                    eta = int(time())

                task = {
                    "eta"          : eta,
                    "kind"         : kind_,
                    "id"           : id_,
                    "args"         : args,
                    # here I use the kv pairs instead of a map to workaround an issue that
                    # empty table will be converted to msgpack array inside lua
                    "kwargs"       : list(kwargs.items()),
                    "has_callback" : False,
                }

                await enqueue(task)

                return task

            def delay_by(secs, args = [], kwargs = {}):
                eta = int(time()) + secs

                return call_at(eta=eta, args=args, kwargs=kwargs)

            def g(*args, **kwargs):
                return call_at(args=list(args), kwargs=kwargs)

            g.call_at  = call_at
            g.delay_by = delay_by

            return g

        return wrapper

    def callback_handler(remote_call, kind = None):
        def wrapper(f):
            kind_ = kind or f"{f.__module__}.{f.__qualname__}"

            handlers[kind_] = f

            async def g(*args, **kwargs):
                id_ = str(uuid4())

                task = {
                    "eta"          : None,
                    "kind"         : kind_,
                    "id"           : id_,
                    "args"         : list(args),
                    "kwargs"       : list(kwargs.items()),
                    "has_callback" : True,
                }

                # the two calls below is not strictly safe, cuz there is a situation
                # that remote callback executed earlier than the second call
                await remote_call(task, *args, **kwargs)
                await wait_for_resolve(task)

                return task

            return g

        return wrapper

    async def search(cursor = 0, size = 10, pred = None):
        next_cursor, taskbs = await redis.hscan(dt_hash_task, cursor=cursor, count=size)

        tasks = (unpackb(taskb) for _, taskb in taskbs)

        if pred is None or next_cursor == 0:
            return next_cursor, list(tasks)

        filtered = list(filter(pred, tasks))

        if len(filtered) >= size:
            return next_cursor, filtered

        total       = []
        curr_cursor = next_cursor
        curr_size   = size
        while next_cursor != 0 and len(total) + len(filtered) < size:
            total.extend(filtered)
            curr_cursor = next_cursor

            rest = size - len(total)
            if len(filtered) == 0:
                fact = 1
            else:
                fact = round(rest / len(filtered))

            if fact > 0:
                curr_size *= 2

            next_cursor, taskbs = await redis.hscan(dt_hash_task, cursor=curr_cursor, count=curr_size)

            tasks    = (unpackb(taskb) for _, taskb in taskbs)
            filtered = list(filter(pred, tasks))

        if next_cursor == 0 or len(total) + len(filtered) == size:
            return next_cursor, total + filtered

        l = 1
        r = curr_size

        while l < r:
            m = int((l + r) / 2)

            next_cursor, taskbs = await redis.hscan(dt_hash_task, cursor=curr_cursor, count=m)

            tasks    = (unpackb(taskb) for _, taskb in taskbs)
            filtered = list(filter(pred, tasks))

            total_len = len(total) + len(filtered)

            if total_len == size:
                return next_cursor, total + filtered
            elif total_len > size:
                r = m
            else:
                l = m + 1

        return next_cursor, total + filtered

    async def handle(task):
        try:
            handler = handlers.get(task["kind"])

            if handler is not None:
                args   = task["args"]
                kwargs = dict(task["kwargs"])

                handler_ret = handler(*args, **kwargs)

                if inspect.iscoroutine(handler_ret):
                    handler_ret = await handler_ret

                if task["has_callback"]:
                    callback_ret = handler_ret(task.get("value", None))

                    if inspect.iscoroutine(callback_ret):
                        await callback_ret
            else:
                logger.warning(f"unknown task of kind: {task['kind']}")

            await ack(task["id"])
            logger.info(repr_task(Stage.acked, task))
        except Exception as e:
            await handle_exception(e)
        finally:
            semaphore.release()

    async def check_process() -> None:
        try:
            wip_tasks = await redis.hgetall(dt_hash_proc)
            now = int(time())

            for id_, idle_from in wip_tasks.items():
                if now - int(idle_from) > max_ttl:
                    await re_enqueue(id_)
        except Exception as e:
            await handle_exception(e)

    async def main():
        counter = 0
        while True:
            try:
                if not stopped:
                    await semaphore.acquire()

                    try:
                        task = await dequeue()

                        if task is not None:
                            if task["eta"] <= int(time()):
                                logger.info(repr_task(Stage.handling, task))

                                create_task(handle(task))
                                continue
                            else:
                                await re_enqueue(task["id"])
                                semaphore.release()
                        else:
                            semaphore.release()
                    except Exception as e:
                        semaphore.release()
                        raise e

                await sleep(1)

                if counter == 0:
                    create_task(check_process())

                # the prime closest to 30
                counter = (counter + 1) % 31
            except Exception as e:
                await handle_exception(e)

    def listen() -> None:
        nonlocal listener_task

        assert listener_task is None, "already listening"

        listener_task = create_task(main())

    async def unlisten() -> None:
        nonlocal listener_task, stopped

        assert listener_task is not None, "not listening"

        stopped = True

        while True:
            total_processing = await redis.hlen(dt_hash_proc)

            if total_processing == 0:
                logger.info("Pending Tasks all done.")
                break

            logger.info(f"Waiting for {total_processing} task(s) to be done...")
            await sleep(1)

        listener_task.cancel()
        listener_task = None

    dispatcher = Dispatcher(
        handler          = handler,
        callback_handler = callback_handler,
        resolve          = resolve,
        listen           = listen,
        unlisten         = unlisten,
        search           = search,
        cancel           = cancel,
        init             = init,
    )

    return dispatcher
