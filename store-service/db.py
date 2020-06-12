import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, String, Integer
)

from settings import config

meta = MetaData()

items = Table(
    'items', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('code', String, nullable=False),
    Column('category', String),
)

async def init_pg(app):
    engine = await aiopg.sa.create_engine(**config['postgres'])
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

