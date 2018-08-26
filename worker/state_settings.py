import logging
from transitions import Machine
from state_helpers import MachineHelpers
import enums

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State:
    """Extends the base state.py.

    Presents user with settings menu.
    """

    def __init__(self):
        super().__init__()
        states = [
            {'name': 'settings_menu', 'on_enter': 'default_on_enter'},
            {'name': 'settings_subscription', 'on_enter': 'default_on_enter'},
            {'name': 'settings_title', 'on_enter': 'default_on_enter'}
        ]

        # Transitions
        transitions = [
            {'trigger': 'settings', 'source': 'idle', 'dest': 'settings_menu'},
            {'trigger': 'subscription', 'source': 'settings_menu', 'dest': 'settings_subscription'},
            {'trigger': 'message', 'source': 'settings_subscrption', 'dest': 'idle',
                'conditions': 'is_proper_subscription', 'before': 'set_user_age'},
            {'trigger': 'title', 'source': 'settings_menu', 'dest': 'settings_title'},
            {'trigger': 'message', 'source': 'settings_title', 'dest': 'idle',
                'conditions': 'is_proper_title', 'before': 'set_user_age'},
        ]

        # Append to Machine
        self.machine_add_states_and_transitions(states, transitions)

    # Conditions
