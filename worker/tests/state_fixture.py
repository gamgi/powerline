import logging
from transitions import Machine
from telegram import ReplyKeyboardRemove

import enums

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State(Machine):
    def __init__(self, bot):
        self.bot = bot
        self.language = 'EN'  # TODO
        states = [
            {'name': 'unregistered'},
            {'name': 'register_1', 'on_enter': 'default_on_enter'},
            {'name': 'register_2', 'on_enter': 'default_on_enter'},
            {'name': 'register_3', 'on_enter': 'default_on_enter'},
            {'name': 'idle'},
            {'name': 'dummy_state'}]

        # User registration transitions
        transitions_register = [
            {'trigger': 'start', 'source': 'unregistered', 'dest': 'register_1'},
            {'trigger': 'message', 'source': 'register_1', 'dest': 'register_2',
             'conditions': 'is_proper_title'},
            {'trigger': 'message', 'source': 'register_2', 'dest': 'register_3',
             'conditions': 'is_proper_age'},
        ]
        # General transitions
        transitions = [
            {'trigger': 'dummy', 'source': '*', 'dest': 'dummy_state'},
            {'trigger': 'joke', 'source': 'idle', 'dest': '=', 'after': 'tell_joke'}
        ]

        Machine.__init__(
            self,
            states=states,
            transitions=transitions + transitions_register,
            send_event=True,
            initial='unregistered')

    # Conditions
    def is_proper_title(self, event):
        message = event.kwargs.get('message').lower()
        if message not in ['mr', 'mrs']:
            return False
        return True

    def is_proper_age(self, event):
        message = event.kwargs.get('message').lower()
        if message not in list(str(range(1, 5))) + ['n']:
            return False
        return True

    # State actions
    def default_on_enter(self, event):
        assert event.transition.dest == self.state
        chat_id = event.kwargs.get('chat_id')
        destination = event.transition.dest.upper()
        # Is there something to say?
        try:
            message = enums.MESSAGES[self.language][destination]
            try:
                keyboard = enums.KEYBOARDS[destination]
            except KeyError:
                keyboard = ReplyKeyboardRemove()

            self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard)
            logging.info('Sent message')
        except KeyError:
            logging.info('Nothing to say')
