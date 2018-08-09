# From http://python-rq.org/patterns/
import os
from urllib.parse import urlparse
from redis import Redis
from redis import exceptions as redis_exceptions
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
import config

from time import sleep

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("worker.internal")
logger.setLevel(logging.INFO)

listen = ['high', 'default', 'low']

redis_url = config.REDIS_URL
if not redis_url:
    raise RuntimeError('Set up Redis first.')

import worker

try:
    conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
    if __name__ == '__main__':
        with Connection(conn):
            worker = Worker(map(Queue, listen))
            worker.work()
except redis_exceptions.ConnectionError:
    logging.error('Unable to connect to redis')
    sleep(10)
