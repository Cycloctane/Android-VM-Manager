from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import redis.asyncio as redis
from os import environ

SQLALCHEMY_DATABASE_URL = environ.get("SQLALCHEMY_DATABASE_URL")

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL % "pymysql", poolclass=NullPool)
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL % "aiomysql",
                                   pool_recycle=3600, pool_size=2, max_overflow=1)

async_db_session = async_sessionmaker(bind=async_engine)

redis_pool = redis.ConnectionPool.from_url(environ.get("REDIS_URL"))

