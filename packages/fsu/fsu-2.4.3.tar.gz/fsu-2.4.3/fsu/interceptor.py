from inspect import signature, Parameter
from functools import wraps

_kinds_p = {
    Parameter.POSITIONAL_ONLY       : 1,
    Parameter.POSITIONAL_OR_KEYWORD : 2,
    Parameter.KEYWORD_ONLY          : 3,
    Parameter.VAR_POSITIONAL        : 4,
    Parameter.VAR_KEYWORD           : 5,
}
def _param_kind_key(p):
    return (_kinds_p[p.kind], 0 if p.default == Parameter.empty else 1)

def adimap(pre = None, post = None):
    def intercept(body):
        body_sig          = signature(body)
        merged_parameters = list(body_sig.parameters.values())

        if pre is not None:
            pre_sig = signature(pre)

            for p0 in pre_sig.parameters.values():
                p1 = next((p1 for p1 in merged_parameters if p0.name == p1.name), None)

                if p1 is not None:
                    if p0.annotation != p1.annotation:
                        raise ValueError("conflict parameters")
                else:
                    merged_parameters.append(p0)

        merged_parameters.sort(key=_param_kind_key)

        handle_sig = body_sig.replace(parameters=merged_parameters)

        @wraps(body)
        async def handle(**kwargs):
            if pre is not None:
                pre_kwargs = { k : kwargs[k] for k in pre_sig.parameters }
                ret = await pre(**pre_kwargs)

            if ret is not None:
                return ret

            body_kwargs = { k : kwargs[k] for k in body_sig.parameters }

            ret = await body(**body_kwargs)

            if post is not None:
                return await post(ret)

            return ret

        handle.__signature__ = handle_sig

        return handle

    return intercept
