import datetime

from aiohttp import web

import db
from settings import config
from utils import gen_json_response, gen_access_refresh_tokens


async def index(request):
    return web.Response(text='Hello world')


async def post_signup(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        if 'email' not in data or 'password' not in data:
            return gen_json_response('Email and password needed', 400)

        cursor = await conn.execute(db.users.select().where(db.users.c.email == data['email']))
        records = await cursor.fetchall()

        if records:
            return gen_json_response('Email already registered', 409)

        cursor = await conn.execute(db.users.insert().values({
            'email': data['email'],
            'password': data['password'],  # TODO: hash password
        }))

        return gen_json_response('OK')


async def post_signin(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        if 'email' not in data or 'password' not in data:
            return gen_json_response('Email and password needed', 400)

        cursor = await conn.execute(db.users.select().where(db.users.c.email == data['email']))
        records = await cursor.fetchall()

        if not records:
            return gen_json_response('No such email', 400)

        user = [dict(i) for i in records][0]

        if user['password'] != data['password']:
            return gen_json_response('Incorrect password', 400)

        access_token, expire_access_token, refresh_token, expire_refresh_token = gen_access_refresh_tokens()

        cursor = await conn.execute(db.users.update().where(db.users.c.email == data['email']).values({
            'access_token': access_token,
            'access_token_expiration_time': expire_access_token,
            'refresh_token': refresh_token,
            'refresh_token_expiration_time': expire_refresh_token,
        }))

        return gen_json_response({'access_token': access_token, 'refresh_token': refresh_token})


async def post_validate(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        if 'access_token' not in data:
            return gen_json_response('Access token needed', 400)

        cursor = await conn.execute(db.users.select().where(db.users.c.access_token == data['access_token']))
        records = await cursor.fetchall()

        if not records:
            return gen_json_response('Invalid access token', 400)

        user = [dict(i) for i in records][0]

        if user['access_token_expiration_time'] < datetime.datetime.now():
            return gen_json_response('Expired access token', 400)

        return gen_json_response('OK')


async def post_refresh(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()

        if 'refresh_token' not in data:
            return gen_json_response('Refresh token needed', 400)

        cursor = await conn.execute(db.users.select().where(db.users.c.refresh_token == data['refresh_token']))
        records = await cursor.fetchall()

        if not records:
            return gen_json_response('Invalid refresh token', 400)

        user = [dict(i) for i in records][0]

        if user['refresh_token_expiration_time'] < datetime.datetime.now():
            return gen_json_response('Expired refresh token', 400)

        access_token, expire_access_token, refresh_token, expire_refresh_token = gen_access_refresh_tokens()

        cursor = await conn.execute(db.users.update().where(db.users.c.id == user['id']).values({
            'access_token': access_token,
            'access_token_expiration_time': expire_access_token,
            'refresh_token': refresh_token,
            'refresh_token_expiration_time': expire_refresh_token,
        }))

        return gen_json_response({'access_token': access_token, 'refresh_token': refresh_token})
