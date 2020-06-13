from aiohttp import web, ClientSession

from settings import config


def clean_data(data, needed_data):
    cleaned_data = {}

    for col in needed_data:
        if col in data:
            cleaned_data[col] = data[col]

    return cleaned_data


def gen_json_response(data, code=200):
    return web.json_response({'code': code, 'response': data}, status=code)


def login_required(func):
    async def wrapped_func(request, *args, **kwargs):
        if request.headers.get('Authorization') is None:
            return gen_json_response('Not authorized', 401)
        async with ClientSession() as session:
            async with session.post(
                    config['auth']['scheme'] + '://' + config['auth']['base_url'] + ':' + str(config['auth']['port']) + '/' +
                    config['auth']['validate_handler'],
                    json={config['auth']['access_token_keyword']: request.headers.get('Authorization')}
            ) as resp:
                if resp.status != 200:
                    return gen_json_response('Not authorized', 401)
        return await func(request, *args, **kwargs)

    return wrapped_func
