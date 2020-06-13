from aiohttp import web

import db
from settings import config
from utils import clean_data, gen_json_response, login_required


async def index(request):
    return web.Response(text='Hello world')


async def get_items_from_db(app, id=None, offset=None, limit=None):
    async with app['db'].acquire() as conn:
        if id is not None:
            cursor = await conn.execute(db.items.select().where(db.items.c.id == id))
            records = await cursor.fetchall()
        elif offset is not None and limit is not None:
            cursor = await conn.execute(db.items.select().order_by(db.items.c.id).offset(offset).limit(limit))
            records = await cursor.fetchall()
        else:
            cursor = await conn.execute(db.items.select().order_by(db.items.c.id))
            records = await cursor.fetchall()

        return records


@login_required
async def get_item(request):
    async with request.app['db'].acquire() as conn:
        if request.match_info.get('id'):
            records = await get_items_from_db(request.app, id=request.match_info.get('id'))
        elif request.rel_url.query.get('page'):
            page = int(request.rel_url.query.get('page')) - 1
            per_page = int(request.rel_url.query.get('per_page', config['constants']['per_page']))

            records = await get_items_from_db(request.app, offset=page * per_page, limit=per_page)
        else:
            records = await get_items_from_db(request.app)

        if records:
            items = [dict(i) for i in records]

            cursor = await conn.execute(db.items.count())
            data = await cursor.fetchall()
            data = [dict(i) for i in data][0]['tbl_row_count']

            return gen_json_response({'items': items, 'count': data})
        else:
            return gen_json_response('Empty set', 404)


@login_required
async def post_item(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        cursor = await conn.execute(db.items.insert().values(
            {'name': data['name'], 'code': data['code'], 'category': data['category']}
        ))

        return gen_json_response('OK')


@login_required
async def del_item(request):
    async with request.app['db'].acquire() as conn:
        if not await get_items_from_db(request.app, id=request.match_info.get('id')):
            return gen_json_response('Not found', 404)

        cursor = await conn.execute(db.items.delete().where(db.items.c.id == request.match_info.get('id')))

        return gen_json_response('OK', 201)


@login_required
async def patch_item(request):
    async with request.app['db'].acquire() as conn:
        if not await get_items_from_db(request.app, id=request.match_info.get('id')):
            return gen_json_response('Not found', 404)

        data = await request.json()
        cleaned_data = clean_data(data, ['name', 'code', 'category'])

        cursor = await conn.execute(db.items.update().where(db.items.c.id == request.match_info.get('id')).values(
            cleaned_data
        ))

        return gen_json_response('OK')
