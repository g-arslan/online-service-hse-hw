from sqlalchemy import create_engine, MetaData

from settings import config
from db import items


DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[items])


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)

