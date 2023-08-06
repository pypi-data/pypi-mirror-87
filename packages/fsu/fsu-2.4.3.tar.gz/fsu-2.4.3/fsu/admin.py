from functools import wraps
import json

from pydantic import ValidationError
from fastapi import FastAPI, Depends, Header
from fastapi.exceptions import HTTPException
from databases import Database

from fsu.internal.util import create_schema, deep_normalize_datetime
from fsu.internal.error import FieldNotExist, ObjectNotExist, UnsupportedOperator
from fsu.internal.schema import ReadMany, ReadOne, UpdateMany, UpdateOne, DeleteMany, DeleteOne, CreateOne, \
                                LoginIn, LoginOut, GetCurrentUserOut
import fsu.internal.error_code as E
from fsu.security import sign_required, jwt_field_required, get_jwt_info
from fsu.wxwork import get_user_by_code
from fsu.sql import bind_enhq, verbose_where, find_table
from fsu.error import handle_universal_logic_error, UniversalLogicError
from fsu.schema import OK
import jwt

# TODO handle foreign key constraint fails when creating, updating or deleting rows

def object_not_exist(o):
    return HTTPException(422, f"object `{o}` not exist")

def field_not_exist(o, f):
    return HTTPException(422, f"field `{f}` of object `{o}` not exist")

def unsupported_operator(op):
    return HTTPException(422, f"operator `{op}` not supported")

def handle_enhq_exception(wrapped):
    @wraps(wrapped)
    async def f(*args, **kwargs):
        try:
            return await wrapped(*args, **kwargs)
        except ObjectNotExist as e:
            raise object_not_exist(e.object)
        except FieldNotExist as e:
            raise field_not_exist(e.object, e.field)
        except UnsupportedOperator as e:
            raise unsupported_operator(e.op)

    return f

def handle_validation_error(wrapped):
    @wraps(wrapped)
    async def f(*args, **kwargs):
        try:
            return await wrapped(*args, **kwargs)
        except ValidationError as e:
            raise HTTPException(422, json.loads(e.json()))

    return f

def make_admin_app(
    corp_id,
    enums,
    jwt_secret,
    metadata,

    get_db,
    get_unicode_redis,
    get_secret_by_uaid,
    get_corp_secret_by_uaid,

    debug = False
):
    app    = FastAPI(openapi_prefix="/admin")
    tables = metadata.tables

    app.add_exception_handler(UniversalLogicError, handle_universal_logic_error)

    if not debug:
        app.middleware("http")(sign_required(ttl=60, get_secret_by_uaid=get_secret_by_uaid))
        admin_required = jwt_field_required("admin_id", jwt_secret)
    else:
        # identity decorator
        admin_required = lambda x : x

    auto_schemas = {
        t : create_schema(tables[t])
        for t in tables
    }
    loose_schemas = {
        t : create_schema(tables[t], "loose")
        for t in tables
    }

    make_enhq = bind_enhq(metadata)

    def deep_normalize_filter(t, f):
        def deep_normalize_filter_(f_):
            if len(f_) == 2:
                return (f_[0], map(deep_normalize_filter_, f_[1]))
            elif len(f_) == 3:
                target_table = find_table(metadata, t, f_[1][:-1])
                field_name   = f_[1][-1]

                if field_name not in target_table.c:
                    raise FieldNotExist(target_table.name, field_name)

                target_schema = loose_schemas[str(target_table.name)]
                m = target_schema(**{ field_name : f_[2] })
                v = m.dict()[field_name]

                return (f_[0], f_[1], v)
            else:
                return f_

        return deep_normalize_filter_(f)

    @app.post("/login", response_model=OK[LoginOut])
    async def login(
        i      : LoginIn,
        x_uaid : str = Header(...),
        db           = Depends(get_db),
        redis        = Depends(get_unicode_redis),
    ):
        corp_secret = await get_corp_secret_by_uaid(x_uaid)

        if corp_secret is None:
            raise HTTPException(401, "invalid X-UAID")

        user_info = await get_user_by_code(corp_id, corp_secret, x_uaid, i.code, redis)

        fsu_admin  = tables["fsu_admin"]
        admin_id   = None
        admin_user = await db.fetch_one(fsu_admin.select().where(fsu_admin.c.user_id == user_info["userid"]))

        if admin_user is None:
            admin_id = await db.execute(fsu_admin.insert().values(
                user_id = user_info["userid"],
                name    = user_info["name"],
            ))
        else:
            admin_id = admin_user[fsu_admin.c.id]

        token = jwt.encode({ "admin_id" : admin_id }, jwt_secret)

        return OK(data=LoginOut(access_token=token))

    @app.get("/user", response_model=OK[GetCurrentUserOut])
    @admin_required
    async def get_current_user(info = Depends(get_jwt_info(jwt_secret)), db = Depends(get_db)):
        admin_id = info.get("admin_id")

        if admin_id is None:
            raise UniversalLogicError(E.INVALID_TOKEN)

        fsu_admin = tables["fsu_admin"]
        enhq      = make_enhq("fsu_admin", GetCurrentUserOut)

        row = await db.fetch_one(enhq.query().where(fsu_admin.c.id == admin_id))

        if row is None:
            raise UniversalLogicError(E.INVALID_TOKEN)

        return OK(data=enhq.dict(row))

    @app.get("/enums")
    @admin_required
    async def get_enums():
        return OK(data=enums)

    @app.post("/read")
    @handle_enhq_exception
    @handle_validation_error
    @admin_required
    async def read_many(i : ReadMany, db : Database = Depends(get_db)):
        enhq = make_enhq(i.object, i.fields_)

        if i.filter is not None:
            enhq.filter(deep_normalize_filter(i.object, i.filter))

        if i.order is not None:
            enhq.sort(i.order)

        sql = enhq.query() \
                .offset((i.page - 1) * i.size) \
                .limit(i.size)

        count_sql = enhq.count()

        data  = [deep_normalize_datetime(enhq.dict(r)) for r in await db.fetch_all(sql)]
        total = await db.fetch_val(count_sql)

        return OK(data=data, total=total)

    @app.post("/read/{id}")
    @handle_enhq_exception
    @admin_required
    async def read_one(id : int, i : ReadOne, db : Database = Depends(get_db)):
        enhq = make_enhq(i.object, i.fields_)

        sql = enhq.filter(("EQ", ["id"], id)).query()

        data = deep_normalize_datetime(enhq.dict(await db.fetch_one(sql)))

        return OK(data=data)

    @app.post("/create")
    @handle_validation_error
    @admin_required
    async def create_one(i : CreateOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise object_not_exist(i.object)

        table  = tables[i.object]
        schema = auto_schemas[i.object]

        v = schema(**dict(i.values))

        sql = table.insert().values(v.dict(exclude_unset=True))
        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/update")
    @handle_enhq_exception
    @handle_validation_error
    @admin_required
    async def update_many(i : UpdateMany, db : Database = Depends(get_db)):
        where_clause = verbose_where(i.object, metadata, deep_normalize_filter(i.object, i.filter))

        table  = tables[i.object]
        schema = loose_schemas[i.object]

        v = schema(**dict(i.values))

        sql = table.update().values(v.dict(exclude_unset=True)).where(where_clause)
        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/update/{id}")
    @handle_validation_error
    @admin_required
    async def update_one(id : int, i : UpdateOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise object_not_exist(i.object)

        table  = tables[i.object]
        schema = loose_schemas[i.object]

        v = schema(**dict(i.values))

        sql = table.update().values(v.dict(exclude_unset=True)).where(table.c.id == id)
        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/delete")
    @handle_enhq_exception
    @handle_validation_error
    @admin_required
    async def delete_many(i : DeleteMany, db : Database = Depends(get_db)):
        where_clause = verbose_where(i.object, metadata, deep_normalize_filter(i.object, i.filter))

        table = tables[i.object]

        sql = table.delete().where(where_clause)
        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/delete/{id}")
    @admin_required
    async def delete_one(id : int, i : DeleteOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise object_not_exist (i.object)

        table = tables[i.object]

        sql = table.delete().where(table.c.id == id)
        ret = await db.execute(sql)

        return OK(data=ret)

    return app
