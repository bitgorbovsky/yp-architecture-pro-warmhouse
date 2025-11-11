'''
Root module of repository
'''

from contextlib import asynccontextmanager

from asyncpg import create_pool
from asyncpg import Pool, Connection

from .. import config

__pool: Pool = None


async def init():
    global __pool
    __pool = await create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=str(config.DB_PASS),
        max_size=config.DB_POOL_MAX_SIZE,
        min_size=config.DB_POOL_MIN_SIZE,
        database=config.DB_NAME
    )

@asynccontextmanager
async def do():
    conn = await __pool.acquire()
    try:
        yield conn
    finally:
        await __pool.release(conn)
