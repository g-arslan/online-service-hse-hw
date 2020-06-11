from aiohttp import web

import db
from settings import config
from utils import clean_data


async def index(request):
    return web.Response(text='Hello world')

async def get_item(request):
    async with request.app['db'].acquire() as conn:
        if request.match_info.get('id'):
            cursor = await conn.execute(db.items.select().where(db.items.c.id == request.match_info.get('id')))
            records = await cursor.fetchall()
        elif request.rel_url.query.get('page'):
            page = int(request.rel_url.query.get('page')) - 1
            per_page = int(request.rel_url.query.get('per_page', config['constants']['per_page']))

            cursor = await conn.execute(db.items.select().order_by(db.items.c.id).offset(page * per_page).limit(per_page))
            records = await cursor.fetchall()
        else:
            cursor = await conn.execute(db.items.select().order_by(db.items.c.id))
            records = await cursor.fetchall()

        if records:
            items = [dict(i) for i in records]
        else:
            items = None
        return web.json_response(items)

async def post_item(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        cursor = await conn.execute(db.items.insert().values(
            {'name': data['name'], 'code': data['code'], 'category': data['category']}
        ))

        return web.Response(text='OK')

async def del_item(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.items.delete().where(db.items.c.id == request.match_info.get('id')))

        return web.Response(text='OK')

async def patch_item(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        cleaned_data = clean_data(data, ['name', 'code', 'category'])

        cursor = await conn.execute(db.items.update().where(db.items.c.id == request.match_info.get('id')).values(
            cleaned_data
        ))

        return web.Response(text='OK')
