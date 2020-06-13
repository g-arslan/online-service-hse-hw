import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, String, Integer, DateTime
)

from settings import config

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('access_token', String),
    Column('access_token_expiration_time', DateTime),
    Column('refresh_token', String),
    Column('refresh_token_expiration_time', DateTime),
)

async def init_pg(app):
    engine = await aiopg.sa.create_engine(**config['postgres'])
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

