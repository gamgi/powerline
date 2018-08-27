import logging
from transitions import Machine
from state_helpers import MachineHelpers
import enums

logger = logging.getLogger(__name__)


class State:
    """Extends the base state.py.

    Presents user with settings menu.
    """

    def __init__(self):
        super().__init__()
        states = [
            {'name': 'settings_menu', 'on_enter': 'default_on_enter'},
            {'name': 'settings_register_3', 'on_enter': 'default_on_enter', 'on_exit': 'default_on_exit'},
            {'name': 'settings_title', 'on_enter': 'default_on_enter'},
            {'name': 'settings_delete', 'on_enter': 'default_on_enter'}
        ]

        # Transitions
        transitions = [
            # From idle
            {'trigger': 'settings', 'source': 'idle', 'dest': 'settings_menu'},
            # Subscription
            {'trigger': 'subscription', 'source': [
                'idle', 'settings_menu'], 'dest': 'settings_register_3'},
            {'trigger': 'message', 'source': 'settings_register_3', 'dest': 'idle',
                'conditions': 'is_proper_subscription', 'before': 'set_user_subscription'},
            {'trigger': 'title', 'source': 'settings_menu', 'dest': 'settings_title'},
            # Title
            {'trigger': 'message', 'source': 'settings_title', 'dest': 'idle',
                'conditions': 'is_proper_title', 'before': 'set_user_age'},
            # Delete
            {'trigger': 'delete', 'source': 'settings_menu', 'dest': 'settings_delete'},
            {'trigger': 'back', 'source': 'settings_delete', 'dest': 'idle'},
            {'trigger': 'yesimsuredelete', 'source': 'settings_delete',
                'dest': 'unregistered', 'before': 'delete_user'},
            # Back
            {'trigger': 'back', 'source': 'settings_menu', 'dest': 'idle'},
        ]

        # Append to Machine
        self.machine_add_states_and_transitions(states, transitions)

    # Conditions

    # Transition actions
    def delete_user(self, event):
        user = event.kwargs.get('user')
        assert user is not None
        logger.info('delete user {}'.format(user.id))
