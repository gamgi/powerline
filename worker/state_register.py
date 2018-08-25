import logging
from transitions import Machine
from state_helpers import MachineHelpers
import enums

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State:
    """Extends the base state.py.

    Presents user with registratin steps:
    """

    def __init__(self):
        states = [
            {'name': 'register_1', 'on_enter': 'default_on_enter'},
            {'name': 'register_2', 'on_enter': 'default_on_enter'},
            {'name': 'register_3', 'on_enter': 'default_on_enter', 'on_exit': 'default_on_exit'}
        ]

        # Transitions
        transitions = [
            {'trigger': 'start', 'source': 'unregistered', 'dest': 'register_1'},
            {'trigger': 'message', 'source': 'register_1', 'dest': 'register_2',
                'conditions': 'is_proper_title', 'before': 'set_user_title'},
            {'trigger': 'message', 'source': 'register_2', 'dest': 'register_3',
                'conditions': 'is_proper_age', 'before': 'set_user_age'},
            {'trigger': 'message', 'source': 'register_3', 'dest': 'idle', 'before': 'set_user_tolerance'},
        ]

        # Append to Machine
        try:
            self.transitions += transitions
        except BaseException:
            self.transitions = transitions
        try:
            self.states += states
        except BaseException:
            self.states = states

    # Conditions
    def is_proper_title(self, event):
        message = event.kwargs.get('message').lower()
        if message not in ['mr', 'mrs']:
            logging.info('not valid')
            return False
        logging.info('valid')
        return True

    def is_proper_age(self, event):
        message = event.kwargs.get('message').lower()
        chat_id = event.kwargs.get('chat_id')
        if message not in list(str(range(1, 5))) + ['n']:
            self.bot.send_message(chat_id=chat_id, text="Sorry that's not a proper age")
            return False
        return True

    # Transition actions
    def set_user_title(self, event):
        message = event.kwargs.get('message').lower()
        user = event.kwargs.get('user')
        user.title = message

    def set_user_age(self, event):
        message = event.kwargs.get('message').lower()
        user = event.kwargs.get('user')
        user.age = message
    # TODO make the set and is_proper to a class

    def set_user_tolerance(self, event):
        message = event.kwargs.get('message').lower()
        user = event.kwargs.get('user')
        user.tolerance = message
