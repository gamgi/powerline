# From http://python-rq.org/patterns/
import os
from redis import Redis
from redis import exceptions as redis_exceptions
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from sqlalchemy import create_engine
import config

from time import sleep

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

listen = ['high', 'default', 'low']

redis_url = config.REDIS_URL
if not redis_url:
    raise RuntimeError('Set up Redis first.')

import worker

try:
    logging.info(
        'attempting to connect to {0} on port {1}'.format(
            config.REDIS_HOST,
            config.REDIS_PORT))
    #logging.info('and the orignal is {}'.format(config.REDIS_URL))
    conn = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD)

    db = create_engine(config.SQLALCHEMY_DATABASE_URI)

    if __name__ == '__main__':
        # Bind worker to db and redis
        worker.bind(db, conn)

        with Connection(conn):
            rq_worker = Worker(map(Queue, listen))
            rq_worker.work()
except redis_exceptions.ConnectionError:
    logging.error('Unable to connect to redis')
    sleep(10)
