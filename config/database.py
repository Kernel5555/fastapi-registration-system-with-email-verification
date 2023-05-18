
from masoniteorm.connections import ConnectionResolver

import logging

logger = logging.getLogger('masoniteorm.connection.queries')

logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

file_handler = logging.FileHandler('logs/logs.txt')

logger.addHandler(file_handler)

logger.addHandler(handler)

from dotenv import load_dotenv

load_dotenv('.env')

import os 

DATABASES = {
    "default": "postgres",
    "postgres": {
        "host" : os.getenv('POSTGRES_DB_HOST'),
        "port" : int(os.getenv('POSTGRES_DB_PORT')),
        "database" : os.getenv("POSTGRES_DB_NAME"),
        "user": os.getenv("POSTGRES_DB_USERNAME"),
        "password" : os.getenv('POSTGRES_DB_PASSWORD'),
        "driver": os.getenv("POSTGRES_DB_DRIVER"),
        "log_queries": True,
    },
    "mysql": {
        "host" : os.getenv("MYSQL_DB_HOST"),
        "user" : os.getenv("MYSQL_DB_USERNAME"),
        "port": int(os.getenv("MYSQL_DB_PORT")),
        "password" : os.getenv("MYSQL_DB_PASSWORD"),
        "log_queries": True,
        "driver": os.getenv("MYSQL_DB_DRIVER"),
        "database": os.getenv("MYSQL_DB_NAME")
    },
    "sqlite": {
        "driver": "sqlite",
        "database" : "masonite.sqlite3",
    }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
