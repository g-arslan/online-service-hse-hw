import os

config = {
    'postgres': {
        'database': os.getenv('DB_DATABASE', 'postgres'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', 5432),
    },
    'mq': {
        'host': os.getenv('MQ_HOST', 'localhost'),
        'port': os.getenv('MQ_PORT', 5672),
        'user': os.getenv('MQ_USER', 'guest'),
        'password': os.getenv('MQ_PASSWORD', 'guest'),
        'email_queue': os.getenv('MQ_EMAIL_QUEUE', 'email'),
    },
    'constants': {
        'token_length': os.getenv('TOKEN_LENGTH', 32),
        'access_token_lifetime': os.getenv('ACCESS_TOKEN_LIFETIME', 300),
        'refresh_token_lifetime': os.getenv('REFRESH_TOKEN_LIFETIME', 60 * 60 * 24),
    }
}

