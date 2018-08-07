import logging
import config
from telegram.ext import Updater
import telegram.error

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if (config.PRODUCTION):
    logging.info("running in PRODUCTION")
logging.info("running {}".format(config.TELEGRAM_TOKEN))

try:
    updater = Updater(token=config.TELEGRAM_TOKEN)
    logging.info(
        "Starting webhook on {}<token>".format(
            config.TELEGRAM_DOMAIN))
    updater.start_webhook(listen="0.0.0.0",
                          port=config.TELEGRAM_PORT,
                          url_path=congig.TELEGRAM_TOKEN)
    updater.bot.set_webhook(
        config.TELEGRAM_DOMAIN +
        congig.TELEGRAM_TOKEN)
    updater.idle()
except telegram.error.InvalidToken as err:
    logging.error(err)
