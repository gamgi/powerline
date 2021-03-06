import logging
# Telegram API
import telegram.error
# State machine
import transitions.core
# from telegram import Bot
import config
# Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError, IntegrityError
import models
# Other
import enums
# Logging
import helpers

logger = logging.getLogger(__name__)
if config.DEVELOPMENT:
    logger.setLevel(logging.DEBUG)


class UserNotFoundError(LookupError):
    pass


class Worker:
    def bind(self, bot, Session, redis, State):
        self.bot = bot
        self.redis = redis
        self.Session = Session
        self.state = State(self.bot)
        logger.debug('worker bound')

    def handle_command_start(self, user_id, update, session):
        logger.info('new user {}'.format(user_id))
        logger.debug("command_start ({})".format(user_id))
        chat_id = update.message.chat_id
        user = self.add_user(
            session,
            user_id,
            update.message.chat.username,
            update.message.chat.first_name)
        success = self.state.trigger("start", user_id=user_id, chat_id=chat_id, user=user)
        if success:
            # Save user on succesful state change
            user.state = self.state.state
            self.save_user(session, user)
            logger.debug('user saved')

    def handle_command(self, user_id, update):
        session = self.Session()
        try:
            command, args = helpers.get_command_and_args_from_update(update)
            chat_id = update.message.chat_id
            assert command is not None
            assert chat_id is not None
            try:
                user = self.get_user(session, user_id)
            except UserNotFoundError:
                self.handle_command_start(user_id, update, session)
                return

            # Load user state
            try:
                self.state.set_state(user.state)
            except ValueError as err:
                # User is in a state that no longer exists
                logger.error(
                    'user {} was in state {} that no loger exists'.format(
                        user_id, user.state))
                user.state = 'idle'
                self.save_user(session, user)
                self.state.set_state(user.state)
                return

            logger.debug("command {} with args {} ({})".format(command, args, user_id))
            try:
                success = self.state.trigger(
                    command,
                    user_id=user_id,
                    chat_id=chat_id,
                    args=args,
                    user=user)
                if success:
                    # Save user on succesful state change
                    user.state = self.state.state
                    self.save_user(session, user)
                    logger.debug('user saved')
            except (AttributeError, transitions.core.MachineError) as err:  # transition does not exist
                logger.error(
                    "Attempted transition '{}' from state '{}' for user {} failed".format(
                        command, self.state.state, user_id))
                logger.error(err)
        except SQLAlchemyError as e:
            session.rollback()
            raise
        except OperationalError as err:
            logger.error("Unable to connect to database: {}".format(err))
        finally:
            session.close()

    def handle_message(self, user_id, update):
        session = self.Session()
        try:
            message = helpers.get_message_from_update(update)
            chat_id = update.message.chat_id
            try:
                user = self.get_user(session, user_id)
            except UserNotFoundError:
                logger.info('user {} not found'.format(user_id))
                self.handle_command_start(user_id, update, session)
                return
            # Load user state
            try:
                self.state.set_state(user.state)
            except ValueError as err:
                # User is in a state that no longer exists
                self.state.set_state('idle')
                logger.error(
                    'user {} was in state {} that no loger exists'.format(
                        user_id, user.state))
                return

            logger.debug('message "{}\" ({})'.format(message, user_id))
            try:
                success = self.state.trigger(
                    "message",
                    user_id=user_id,
                    chat_id=chat_id,
                    message=message,
                    user=user)
                if success:
                    # Save user on succesful state change
                    user.state = self.state.state
                    self.save_user(session, user)
                    logger.debug('user saved')
            except (AttributeError, transitions.core.MachineError) as err:  # transition does not exist
                logger.error(
                    "Attempted transition '{}' from state '{}' for user {} failed".format(
                        'message', self.state.state, user_id))
                logger.error(err)
        except SQLAlchemyError as e:
            session.rollback()
            raise
        except OperationalError as err:
            logger.error("Unable to connect to database: {}".format(err))
        finally:
            session.close()

    def get_user(self, session, user_id):
        user = session.query(models.User).get(user_id)
        if (not user):
            raise UserNotFoundError
        return user

    def save_user(self, session, user):
        session.add(user)
        session.commit()

    def add_user(self, session, user_id, username, first_name):
        user = models.User(id=user_id, username=username, first_name=first_name)
        session.add(user)
        session.commit()
        return user


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
