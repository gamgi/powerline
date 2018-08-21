import logging
import config
# Telegram API
from telegram.ext import Updater, CommandHandler, Handler
from telegram.ext import MessageHandler, Filters
import telegram.error
from any_command_handler import AnyCommandHandler
# Redis Queue
from rq import Queue
from redis import Redis
from redis import exceptions as redis_exceptions

from telegram import Update

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


try:
    q = Queue(
        connection=Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD))
except redis_exceptions.ConnectionError:
    logging.error('Unable to connect to redis')

# Helpers


def get_command_from_update(update):
    try:
        return update.message.text.partition(" ")[0]
    except BaseException:
        return None


def get_message_from_update(update):
    try:
        return update.message.text
    except BaseException:
        return None

# Handlers


def start(bot, update):
    """Send a message when the command /start is issued."""
    logging.info('start')
    update.message.reply_text('Hi!')
    try:
        user_id = update.message.from_user.id
    except AttributeError:
        # No from_user means message is from a channel
        return
    result = q.enqueue(
        'worker.handle_command_start', user_id, update)


def any_command(bot, update, args):
    command = get_command_from_update(update)
    logging.info('command ' + command + ' with args ' + args)
    update.message.reply_text('Hi!')
    try:
        user_id = update.message.from_user.id
    except AttributeError:
        # No from_user means message is from a channel
        return
    result = q.enqueue(
        'worker.handle_command', user_id, update, command, args)


def message(bot, update):
    message = get_message_from_update(update)
    logging.info("message {}".format(message))
    try:
        user_id = update.message.from_user.id
    except AttributeError:
        # No from_user means message is from a channel
        return
    result = q.enqueue(
        'worker.handle_message', user_id, update, message)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if (config.TELEGRAM_DOMAIN[-1:] != "/"):
    logging.warning(
        "TELEGRAM_DOMAIN does not end in '/', this might cause issues")

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
    #dispatcher.add_handler(CommandHandler("start", start))
    # for command in commands:
    #    dispatcher.add_handler(CommandHandler(command, any_command, pass_args=True))
    dispatcher.add_handler(CommandHandler("start", start))
    # Possibly replace with
    #dispatcher.add_handler(MessageHandler(Filters.command, any_command))
    dispatcher.add_handler(AnyCommandHandler(any_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message))
    dispatcher.add_error_handler(error)

    updater.idle()
except telegram.error.InvalidToken as err:
    logging.error(err)
