from fastapi.responses import ORJSONResponse

class UniversalLogicError(Exception):
    def __init__(self, error, msg = None):
        self.error = error
        self.msg   = msg

def isDuplicateEntry(e):
    return e.args[0] == 1062

def isMissingForeignKey(e):
    return e.args[0] == 1452

async def handle_universal_logic_error(req, exc : UniversalLogicError):
    return ORJSONResponse({
        "data"  : None,
        "error" : exc.error,
        "msg"   : exc.msg,
    })
