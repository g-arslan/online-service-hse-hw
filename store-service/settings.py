import os

config = {
    'postgres': {
        'database': os.getenv('DB_DATABASE', 'postgres'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', 5432),
    },
    'constants': {
        'per_page': 10,
    },
}

