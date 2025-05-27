from datetime import time

import redis
import logging
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))


def wait_for_redis(host=HOST, port=PORT, retries=0, delay=2):
    for i in range(retries):
        try:
            pool = redis.ConnectionPool(host=host, port=port)
            client = redis.Redis(connection_pool=pool, decode_responses=True)
            client.ping()
            return client
        except redis.ConnectionError:
            logging.warning("Redis connection error")
            time.sleep(delay)


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
