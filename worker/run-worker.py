# From http://python-rq.org/patterns/
import os
from redis import Redis
from redis import exceptions as redis_exceptions
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

from time import sleep

from telegram import Bot

import logging

if config.DEVELOPMENT:
    logging.basicConfig(
        level=logging.INFO,
        format='%(name)-16.15s %(levelname)-7.7s %(module)-13.13s %(message)s')
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(name)-16.16s %(levelname)-7.7s %(message)s')

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

listen = ['high', 'default', 'low']

redis_url = config.REDIS_URL
if not redis_url:
    raise RuntimeError('Set up Redis first.')
from state import State
import worker

if __name__ == '__main__':
    try:
        logger.info(
            'attempting to connect to redis at {0} on port {1}'.format(
                config.REDIS_HOST,
                config.REDIS_PORT))

        redis = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            password=config.REDIS_PASSWORD)

        logger.info(
            'attempting to connect to database at {}'.format(
                config.SQLALCHEMY_DATABASE_URI))
        db = create_engine(config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=db)

        # Note: no additional config required due to webhook.py
        # sending required values to telegram
        bot = Bot(config.TELEGRAM_TOKEN)

        # Bind worker to db and redis
        worker.bind(bot, Session, redis, State)

        with Connection(redis):
            rq_worker = Worker(map(Queue, listen))

            # Set final logging things
            logging.getLogger('rq.worker').setLevel(logging.WARNING)
            logging.getLogger('telegram*').setLevel(logging.WARNING)
            # if not config.DEVELOPMENT:
            #    logging.getLogger('transitions').setLevel(logging.WARNING)

            logger.info('worker started')
            rq_worker.work()
    except redis_exceptions.ConnectionError:
        logger.error('Unable to connect to redis')
        sleep(10)
