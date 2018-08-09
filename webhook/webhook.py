import logging
import config
# Telegram API
from telegram.ext import Updater, CommandHandler
import telegram.error
# Redis Queue
from rq import Queue
from redis import Redis
from redis import exceptions as redis_exceptions

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    q = Queue(connection=Redis(host=config.REDIS_HOST, port=config.REDIS_PORT))
except redis_exceptions.ConnectionError:
    logging.error('Unable to connect to redis')


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    result = q.enqueue(
	'worker.handle_update', update)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if (config.PRODUCTION):
    logging.info("running in PRODUCTION")

try:
    updater = Updater(token=config.TELEGRAM_TOKEN)
    logging.info(
        "Starting webhook on {0}<token>:{1}".format(
            config.TELEGRAM_DOMAIN, config.TELEGRAM_PORT))
    updater.start_webhook(listen="0.0.0.0",
                          port=config.TELEGRAM_PORT,
                          url_path=config.TELEGRAM_TOKEN)
    updater.bot.set_webhook(
        config.TELEGRAM_DOMAIN +
        config.TELEGRAM_TOKEN)

    # Connect the commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_error_handler(error)

    updater.idle()
except telegram.error.InvalidToken as err:
    logging.error(err)
