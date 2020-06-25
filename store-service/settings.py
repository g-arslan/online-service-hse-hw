import os

config = {
    'postgres': {
        'database': os.getenv('DB_DATABASE', 'postgres'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', 5432),
    },
    'auth': {
        'scheme': os.getenv('AUTH_SCHEME', 'http'),
        'base_url': os.getenv('AUTH_HOST', 'localhost'),
        'port': os.getenv('AUTH_PORT', 8080),
        'validate_handler': os.getenv('AUTH_VALIDATE_HANDLER', 'validate'),
        'access_token_keyword': os.getenv('AUTH_ACCESS_TOKEN_KEYWORD', 'access_token')
    },
    'constants': {
        'per_page': 10,
    },
}

