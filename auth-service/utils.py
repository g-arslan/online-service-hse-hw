import datetime
import secrets

from aiohttp import web

from settings import config


def gen_json_response(data, code=200):
    return web.json_response({'code': code, 'response': data}, status=code)


def gen_access_refresh_tokens(token_length=config['constants']['token_length'],
                              access_token_lifetime=config['constants']['access_token_lifetime'],
                              refresh_token_lifetime=config['constants']['refresh_token_lifetime']):
    now = datetime.datetime.now()
    return (secrets.token_urlsafe(token_length),
            now + datetime.timedelta(seconds=access_token_lifetime),
            secrets.token_urlsafe(token_length),
            now + datetime.timedelta(seconds=refresh_token_lifetime),
            )
