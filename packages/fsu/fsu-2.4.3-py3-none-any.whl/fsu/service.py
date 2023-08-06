from typing import Dict, NamedTuple, Callable, Literal, Awaitable, TypeVar, Optional, List, Any
from asyncio import Future

T = TypeVar("T")

class ServiceProvider(NamedTuple):
    add     : Callable[[
            str,
            Callable[..., Awaitable[T]],
            Optional[Callable[[T], Awaitable[None]]],
            Optional[Callable[[T], Awaitable[None]]],
            List[str],
        ],
        "Future[T]"
    ]
    init    : Callable[[], Awaitable[None]]
    destroy : Callable[[], Awaitable[None]]
    getter  : Callable[[str], Callable[[], Any]]

def make_service_provider() -> ServiceProvider:
    stage : Literal["idle", "init"] = "idle"

    srvs     : Dict[str, Any]           = {}
    futs     : Dict[str, "Future[Any]"] = {}
    srv_deps : Dict[str, List[str]]     = {}

    creates  : Dict[str, Callable[..., Awaitable[T]]]    = {}
    inits    : Dict[str, Callable[[T], Awaitable[None]]] = {}
    destroys : Dict[str, Callable[[T], Awaitable[None]]] = {}

    top_sort    : List[str] = []
    out_degrees : Dict[str, int] = {}

    def add(
        name    : str,
        create  : Callable[[List[Any]], Awaitable[T]],
        init    : Optional[Callable[[T], Awaitable[None]]] = None,
        destroy : Optional[Callable[[T], Awaitable[None]]] = None,
        deps    : List[str] = [],
    ) -> "Future[T]":
        assert stage == "idle", "adding service after getting initialized"

        creates[name]  = create
        srv_deps[name] = deps

        if name not in out_degrees:
            out_degrees[name] = 0
        for dep in deps:
            if dep not in out_degrees:
                out_degrees[dep] = 0

            out_degrees[dep] += 1

        if init is not None:
            inits[name] = init

        if destroy is not None:
            destroys[name] = destroy

        fut : "Future[T]" = Future()
        futs[name] = fut

        return fut

    async def init() -> None:
        nonlocal stage
        nonlocal futs
        nonlocal out_degrees

        assert stage == "idle", "already initialized"

        while len(top_sort) < len(srv_deps):
            s = min(out_degrees, key=lambda k: out_degrees[k])
            assert out_degrees[s] == 0, "cyclic dependency not supported"

            top_sort.insert(0, s)
            del out_degrees[s]

            for dep in srv_deps[s]:
                if dep not in srv_deps:
                    raise KeyError(f"no service named {dep} found")

                out_degrees[dep] -= 1

        for name in top_sort:
            f = creates[name]
            dep_srvs = (srvs[dep_name] for dep_name in srv_deps[name])

            srv : Any  = await f(*dep_srvs)
            srvs[name] = srv
            futs[name].set_result(srv)

            if name in inits:
                await inits[name](srv)

        del futs
        del out_degrees

        stage = "init"

    async def destroy() -> None:
        assert stage == "init", "not initialized"

        for name in reversed(top_sort):
            if name in destroys:
                await destroys[name](srvs[name])

    def getter(name : str) -> Callable[[], Any]:
        if name not in srv_deps:
            raise KeyError(f"no service named {name} found")

        def get_srv() -> Any:
            assert stage == "init", "not initialized"

            return srvs[name]

        return get_srv

    return ServiceProvider(
        add     = add,
        init    = init,
        destroy = destroy,
        getter  = getter,
    )
