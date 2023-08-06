import aiohttp

from fsu.error import UniversalLogicError
import fsu.internal.error_code as E

async def get_user_by_code(corp_id : str, corp_secret : str, uaid : str, code : str, redis):
    redis_key    = "fsu.wxwork.access_token:<{uaid}>"
    access_token = await redis.get(redis_key)

    async with aiohttp.ClientSession() as session:
        if access_token is None:
            params = {
                "corpid"     : corp_id,
                "corpsecret" : corp_secret,
            }
            async with session.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken", params=params) as resp:
                data = await resp.json()

                if "errcode" in data and data["errcode"] != 0:
                    raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

                access_token = data["access_token"]
                expires_in   = data["expires_in"]

                tr = redis.multi_exec()
                tr.set(redis_key, access_token)
                tr.expire(redis_key, expires_in - 200)
                ok1, ok2 = await tr.execute()
                assert ok1
                assert ok2

        params = {
            "access_token" : access_token,
            "code"         : code,
        }
        async with session.get("https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo", params=params) as resp:
            data = await resp.json()

            if "errcode" in data:
                errcode = data["errcode"]

                # invalid token
                if errcode == 42001:
                    await redis.delete(redis_key)
                    return await get_user_by_code(corp_id, corp_secret, uaid, code, redis)

                if errcode != 0:
                    raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

            if "UserId" not in data:
                raise UniversalLogicError(E.LOGIN_FAILED, "not a member")

            user_id = data["UserId"]

        params = {
            "access_token" : access_token,
            "userid"       : user_id,
        }
        async with session.get("https://qyapi.weixin.qq.com/cgi-bin/user/get", params=params) as resp:
            data = await resp.json()

            if "errcode" in data:
                errcode = data["errcode"]

                # invalid token
                if errcode == 42001:
                    await redis.delete(redis_key)
                    return await get_user_by_code(corp_id, corp_secret, uaid, code, redis)

                if errcode != 0:
                    raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

            return data
