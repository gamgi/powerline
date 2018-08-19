# Telegram API
import telegram.error
# State machine
from state import State
# from telegram import Bot
import config
# Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
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


class Worker:
    def bind(self, bot, Session, redis):
        self.bot = bot
        self.redis = redis
        self.Session = Session
        self.state = State(self.bot)

    def command_start(self, user_id, update):
        logging.debug("command_start ({})".format(user_id))
        self.bot.send_message(
            chat_id=update.message.chat_id,
            text=enums.MESSAGES['EN'].START_HELLO_MESSAGE.value)
        # Save user to DB if new
        try:
            session = self.Session()
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
        except OperationalError:
            logging.error("Unable to connect to database")
        # state.user.trigger("next")

    def handle_command(self, user_id, update, command, args):
        chat_id = update.message.chat_id
        # Check is registered
        # Check state nad set self.state.set_state('unregistered')
        logging.info(
            "command {} with args {} ({})".format(
                command, args, user_id))
        try:
            self.state.trigger(command, user_id=user_id, chat_id=chat_id)
            logging.info('new state is {}'.format(self.state.state))
            # success, make menu of possible commands via
            # m.get_triggers(self.state.state)
        except Exception as err:
            logging.error(err)

    def handle_message(self, user_id, update, message):
        chat_id = update.message.chat_id
        # Check is registered
        # Check state nad set self.state.set_state('unregistered')

        logging.info(
            "message {} ({})".format(
                message, user_id))
        try:
            pass
            # self.state.trigger(command)
            #logging.info('new state is {}'.format(self.state.state))
            # success, make menu of possible commands via
            # m.get_triggers(self.state.state)
        except Exception as err:
            logging.error(err)

# Hacky-solution for production. Python-rq does not allow queueing instances, but
# instantiating the worker in the module is allowed.
# Having the worker as a class makes testing easier.


worker = Worker()


def command_start(*args):
    worker.command_start(*args)


def handle_command(*args):
    worker.handle_command(*args)


def handle_message(*args):
    worker.handle_message(*args)


def bind(*args):
    worker.bind(*args)
