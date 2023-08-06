from sqlalchemy import TIMESTAMP, Column, Index, Integer, func

TSZ = TIMESTAMP(timezone=True)

def common_columns():
    fncurtz = func.current_timestamp()

    return [
        Column("id"        , Integer, primary_key=True, autoincrement=True)    ,
        Column("created_at", TSZ    , nullable=False  , server_default=fncurtz),
        Column("updated_at", TSZ    , nullable=False  , server_default=fncurtz , onupdate=fncurtz),

        Index(None, "created_at"),
        Index(None, "updated_at"),
    ]
