# Telegram API
from telegram.ext import Updater, CommandHandler
import telegram.error
#from telegram import Bot
import config

# Logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("worker.internal")
#logger = logging.getLogger('rq.worker')
logger.setLevel(logging.INFO)


# Preload
def connect_database():
    logging.info("Connecintg DB")
    return True


db = connect_database()
#bot = Bot(config.TELEGRAM_TOKEN)


def handle_update(bot, update):
    logging.info("Handling job")
    bot.send_message(chat_id=update.message.chat_id, text="Hi there!")
    return True
