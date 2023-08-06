from sqlalchemy import Table, Column
from sqlalchemy import String
from fsu.model import common_columns

def connect_admin_model(metadata):
    FsuAdmin = Table("fsu_admin", metadata, *common_columns(),
        Column("user_id", String(64), nullable=False , unique=True),
        Column("name"   , String(20), nullable=False),
    )
