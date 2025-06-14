import time
import redis
import logging
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()]
    )


def wait_for_redis(retries=5, delay=2):
    for i in range(retries):
        try:
            client = redis.Redis(host=HOST, port=PORT, decode_responses=True, health_check_interval=30)
            client.ping()
            logging.info("Connected to Redis on attempt %d", i + 1)
            return client
        except redis.ConnectionError as e:
            logging.warning("Redis connection attempt %d failed: %s", i + 1, e)
            time.sleep(delay)
    raise ConnectionError(f"Could not connect to Redis at {HOST}:{PORT} after {retries} attempts.")


setup_logger()
