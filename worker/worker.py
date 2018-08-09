# Telegram API
from telegram.ext import Updater, CommandHandler
import telegram.error
from telegram import Bot
import config

# Logging
import logging
logger = logging.getLogger()
#logger = logging.getLogger('rq.worker')
logger.setLevel(logging.INFO)


# Preload
def connect_database():
    logging.info("Connecintg DB")
    return True


db = connect_database()
bot = Bot(config.TELEGRAM_TOKEN)


def handle_update(client, update):
    logging.info("Handling job from {0}: {1}".format(client, message))
    bot.send_message(chat_id=update.message.chat_id, text="Hi there!")
    return True
