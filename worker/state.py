import logging
from redis import StrictRedis
from transitions import Machine
from telegram import ReplyKeyboardRemove

import enums

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State(Machine):
    # self.is_waiting_message=True
    # def save_to_db
    def __init__(self, bot):
        self.bot = bot
        self.language = 'EN'  # TODO
        states = [
            'unregistered',
            {'name': 'register_1', 'on_enter': 'default_on_enter'},
            {'name': 'register_2', 'on_enter': 'default_on_enter'},
            {'name': 'register_3', 'on_enter': 'default_on_enter'},
            'idle',
            'dummy_state']

        commands = [{'trigger': 'dummy',
                     'source': '*',
                     'dest': 'dummy_state'},
                    {'trigger': 'start',
                     'source': 'unregistered',
                     'dest': 'register_1'},
                    {'trigger': 'message',
                     'source': 'register_1',
                     'dest': 'register_2',
                     'conditions': 'is_proper_title'},
                    {'trigger': 'message',
                     'source': 'register_2',
                     'dest': 'register_3',
                     'conditions': 'is_proper_age'},
                    ]
        transitions = [
            # lump.heat(answer=74)
            # {'trigger': 'check_a', 'source': 'unregistered', 'dest': None, conditions=is_proper_x},
            # {'trigger': 'check_a', 'source': 'register_1', 'dest': 'register_w', conditions=y},
            # define quesiton on enter. write on exit
            {'trigger': 'ask_a', 'source': 'unregistered', 'dest': 'register_1'},
            {'trigger': 'ask_b', 'source': 'register_1', 'dest': 'register_2'},
            {'trigger': 'ask_c', 'source': 'register_2', 'dest': 'register_3'},
            {'trigger': 'complete_register', 'source': 'register_3', 'dest': 'idle'},
        ]
        Machine.__init__(
            self,
            states=states,
            transitions=transitions +
            # after_state_change --> save to db
            commands,
            send_event=True,
            initial='unregistered')

    """
    def on_enter_register_1(self, event):
        chat_id = event.kwargs.get('chat_id')
        assert chat_id is not None
        assert user_lang is not None

        self.bot.send_message(
            chat_id=chat_id,
            text=enums.MESSAGES[self.language].REGISTER_1.value,
            reply_markup=enums.KEYBOARDS.REGISTER_1_KEYBOARD.value)
    """

    def is_proper_title(self, event):
        message = event.kwargs.get('message').lower()
        if message not in ['mr', 'mrs']:
            return False
        return True

    def is_proper_age(self, event):
        message = event.kwargs.get('message').lower()
        if message not in range(1, 5) + ['n']:
            return False
        return True

    def default_on_enter(self, event):
        chat_id = event.kwargs.get('chat_id')
        destination = event.transition.dest
        assert destination == self.state
        # Is there something to say?
        try:
            message = enums.MESSAGES[self.language][destination.upper()].value
            try:
                keyboard = enums.KEYBOARDS['{}_KEYBOARD'.format(
                    destination.upper())].value
            except KeyError:
                keyboard = ReplyKeyboardRemove()

            self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard)
            logging.info('Sent message')
        except KeyError:
            logging.info('Nothing to say')
