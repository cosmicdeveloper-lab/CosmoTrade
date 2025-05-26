import redis
import logging
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))

pool = redis.ConnectionPool(host=HOST, port=PORT)
r = redis.Redis(connection_pool=pool, decode_responses=True)


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
