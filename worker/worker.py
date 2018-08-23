# Telegram API
import telegram.error
# State machine
import transitions.core
# from telegram import Bot
import config
# Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError
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
import helpers


class UserNotFoundError(LookupError):
    pass


class Worker:
    def bind(self, bot, Session, redis, State):
        self.bot = bot
        self.redis = redis
        self.Session = Session
        self.state = State(self.bot)
        logging.info('Worker bound')

    def handle_command_start(self, user_id, update):
        logging.debug("command_start ({})".format(user_id))
        chat_id = update.message.chat_id
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
            try:
                success = self.state.trigger(
                    "start", user_id=user_id, chat_id=chat_id)
                if success:
                    user.state = self.state.state
                    self.save_user(user)
                logging.info('new state is {}'.format(self.state.state))
            except transitions.core.MachineError as err:  # transition does not exist
                logging.error(
                    "Attempted transition '{}' from state '{}' for user {} failed".format(
                        'start', self.state.state, user_id))
                logging.error(err)
        except OperationalError as err:
            logging.error("Unable to connect to database: {}".format(err))
            raise
        except ProgrammingError as err:
            logging.error("Database schema error: {}".format(err))
            raise

    def handle_command(self, user_id, update):
        command, args = helpers.get_command_and_args_from_update(update)
        chat_id = update.message.chat_id
        assert command is not None
        assert chat_id is not None
        user = self.get_user(user_id)
        # Check is registered
        # Check state nad set self.state.set_state('unregistered')
        self.state.set_state(user.state)

        logging.info(
            "command {} with args {} ({})".format(
                command, args, user_id))
        try:
            try:
                success = self.state.trigger(
                    command,
                    user_id=user_id,
                    chat_id=chat_id,
                    args=args)
                if success:
                    logging.info('new state is {}'.format(self.state.state))
                    user.state = self.state.state
                    self.save_user(user)
                # success, make menu of possible commands via
                # m.get_triggers(self.state.state)
            except transitions.core.MachineError as err:  # transition does not exist
                logging.error(
                    "Attempted transition '{}' from state '{}' for user {} failed".format(
                        command, self.state.state, user_id))
                logging.error(err)
        except OperationalError as err:
            logging.error("Unable to connect to database: {}".format(err))
            raise
        except ProgrammingError as err:
            logging.error("Database schema error: {}".format(err))
            raise

    def handle_message(self, user_id, update):
        message = helpers.get_message_from_update(update)
        chat_id = update.message.chat_id
        user = self.get_user(user_id)
        self.state.set_state(user.state)

        logging.info(
            'message "{}\" ({})'.format(
                message, user_id))
        try:
            try:
                success = self.state.trigger(
                    "message",
                    user_id=user_id,
                    chat_id=chat_id,
                    message=message)
                if success:
                    logging.info('new state is {}'.format(self.state.state))
                    user.state = self.state.state
                    self.save_user(user)
                else:
                    logging.info('no change')
            except transitions.core.MachineError as err:  # transition does not exist
                logging.error(
                    "Attempted transition '{}' from state '{}' for user {} failed".format(
                        'message', self.state.state, user_id))
                logging.error(err)
        except OperationalError as err:
            logging.error("Unable to connect to database: {}".format(err))
            raise
        except ProgrammingError as err:
            logging.error("Database schema error: {}".format(err))
            raise

    def get_user(self, user_id):
        try:
            session = self.Session()
            user = session.query(models.User).get(user_id)
            if (not user):
                raise UserNotFoundError
            session.close()
            return user
        except OperationalError:
            logging.error("Unable to connect to database")

    def save_user(self, user):
        try:
            session = self.Session()
            try:
                session.add(user)
                session.commit()
            except SQLAlchemyError as e:
                logging.error(e)
            session.close()
        except OperationalError:
            logging.error("Unable to connect to database")


# Hacky-solution for production. Python-rq does not allow queueing instances, but
# instantiating the worker in the module is allowed.
# Having the worker as a class makes testing easier.


worker = Worker()


def handle_command_start(*args):
    worker.handle_command_start(*args)


def handle_command(*args):
    worker.handle_command(*args)


def handle_message(*args):
    worker.handle_message(*args)


def bind(*args):
    worker.bind(*args)
