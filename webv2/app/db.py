import redis.asyncio as redis
from configparser import ConfigParser

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

REDIS_URL = conf.get('fastapi', 'redis_url')

redis_pool = redis.ConnectionPool.from_url(REDIS_URL)

