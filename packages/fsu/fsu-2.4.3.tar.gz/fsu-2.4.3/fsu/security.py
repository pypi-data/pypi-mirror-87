import math
import hmac
from time import time

from fastapi import Request, Depends, Header
from fastapi.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler
from fsu.interceptor import adimap
from fsu.error import UniversalLogicError
import fsu.internal.error_code as E
import jwt

def generate_sign(secret, ts, data):
    to_be_signed = f"{data}.{ts}"

    return hmac.digest(secret.encode(), to_be_signed.encode(), "sha256").hex()

def sign_required(get_secret_by_uaid, ttl):
    async def middleware(request : Request, call_next):
        headers = request.headers

        if any(k not in headers for k in ["x-uaid", "x-timestamp", "x-signature"]):
            return await http_exception_handler(request, HTTPException(422, "missing required header X-UAID, X-Timestamp or X-Signature"))

        secret = await get_secret_by_uaid(headers["x-uaid"])

        if secret is None:
            return await http_exception_handler(request, HTTPException(401, "invalid X-UAID"))

        x_ts       = int(headers["x-timestamp"])
        current_ts = math.floor(time())
        if current_ts - x_ts > ttl:
            return await http_exception_handler(request, HTTPException(425, "too early"))

        if request.method == "GET":
            data = str(request.query_params)
        else:
            data = (await request.body()).decode()

            # create a new request with the new receive cuz we can only read from request body for a single time
            async def receive(*args, **kwargs):
                return {
                    "type": "http.request",
                    "body": data.encode(),
                }
            request = Request(request.scope, receive)

        sign = generate_sign(secret, x_ts, data)

        if sign != headers["x-signature"]:
            return await http_exception_handler(request, HTTPException(400, "bad signature"))

        return await call_next(request)

    return middleware


def get_jwt_info(jwt_secret, invalid_token_error = E.INVALID_TOKEN):
    def f(authorization : str = Header(...)):
        token = None
        info  = None

        s = authorization.find("Bearer")
        if s >= 0:
            token = authorization.replace("Bearer ", "")

        if token is not None:
            try:
                info = jwt.decode(token, jwt_secret)
            except:
                pass

        if info is None:
            raise UniversalLogicError(invalid_token_error)

        return info

    return f


def get_jwt_field(field, jwt_secret, invalid_token_error = E.INVALID_TOKEN, field_not_exist_error = E.INVALID_TOKEN):
    def f(info = Depends(get_jwt_info(jwt_secret, invalid_token_error))):
        if field not in info:
            raise UniversalLogicError(field_not_exist_error)

        return info[field]

    return f


def jwt_field_required(field, jwt_secret, invalid_token_error = E.INVALID_TOKEN, field_not_exist_error = E.INVALID_TOKEN):
    async def f(field_value = Depends(get_jwt_field(field, jwt_secret, invalid_token_error, field_not_exist_error))):
        pass

    return adimap(f)
