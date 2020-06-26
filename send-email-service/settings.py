import os

config = {
    'mq': {
        'host': os.getenv('MQ_HOST', 'localhost'),
        'port': os.getenv('MQ_PORT', 5672),
        'user': os.getenv('MQ_USER', 'guest'),
        'password': os.getenv('MQ_PASSWORD', 'guest'),
        'email_queue': os.getenv('MQ_EMAIL_QUEUE', 'email'),
    },
}

