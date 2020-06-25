import json

import pika
import logging

from settings import config


logger = logging.getLogger(__name__)


def send_email_callback(channel, method, properties, body):
    data = json.loads(body)
    print('Email sent to {}, link is http://localhost:8081/activate/{}'.format(data['email'], data['activate_url']))
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials(config['mq']['user'], config['mq']['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        config['mq']['host'],
        config['mq']['port'],
        '/',
        credentials,
    ))

    channel = connection.channel()
    channel.queue_declare(queue=config['mq']['email_queue'])

    channel.basic_consume(queue=config['mq']['email_queue'], on_message_callback=send_email_callback)
    print('Starting email consuming')
    channel.start_consuming()


if __name__ == '__main__':
    main()
