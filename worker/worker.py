# Telegram API
import telegram.error
# State machine
import state
# from telegram import Bot
import config
# Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import models
# Other
import enums
# Logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("worker.internal")
# logger = logging.getLogger('rq.worker')
logger.setLevel(logging.INFO)


def command_start(user_id, update):
    logging.debug("command_start ({})".format(user_id))
    bot.send_message(chat_id=update.message.chat_id,
                     text=enums.MESSAGES['EN'].START_HELLO_MESSAGE)
    # Save user to DB if new
    session = Session()
    user = session.query(models.User).get(user_id)
    if (not user):
        try:
            user = models.User(
                id=user_id,
                username=update.message.chat.username,
                first_name=update.message.chat.first_name)
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            logging.error(e)
    session.close()


def bind(new_bot, new_db_engine, new_redis):
    global bot, db, redis, Session
    bot = new_bot
    db = new_db_engine
    redis = new_redis
    Session = sessionmaker()
    Session.configure(bind=db)
