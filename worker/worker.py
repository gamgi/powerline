# Telegram API
from telegram.ext import Updater, CommandHandler
import telegram.error
#from telegram import Bot
import config
# Database
from sqlalchemy import create_engine

# Logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("worker.internal")
#logger = logging.getLogger('rq.worker')
logger.setLevel(logging.INFO)

def handle_update(bot, update):
    logging.info("Handling job")
    bot.send_message(chat_id=update.message.chat_id, text="Hi there!")
    return True


db = None
redis = None


def bind(new_db, new_redis):
    global db, redis
    db = new_db
    redis = new_redis

#bot = Bot(config.TELEGRAM_TOKEN)
