import redis
import logging
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))

r = redis.Redis(host=HOST, port=PORT, decode_responses=True)


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
