'''
Service Config
'''

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", default=None)
DB_PASS = config("DB_PASS", cast=Secret, default=None)
DB_NAME = config("DB_NAME", default=None)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
