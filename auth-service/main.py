import pika as pika
from aiohttp import web

from routes import setup_routes
from settings import config
from db import init_pg, close_pg


async def init_mq(app):
    credentials = pika.PlainCredentials(config['mq']['user'], config['mq']['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        config['mq']['host'],
        config['mq']['port'],
        '/',
        credentials,
    ))

    channel = connection.channel()
    channel.queue_declare(queue=config['mq']['email_queue'])

    app['mq'] = connection
    app['channel'] = channel

async def close_mq(app):
    app['mq'].close()

def main():
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(init_pg)
    app.on_startup.append(init_mq)
    app.on_cleanup.append(close_pg)
    app.on_cleanup.append(close_mq)
    web.run_app(app)

if __name__ == '__main__':
    main()
