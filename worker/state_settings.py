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
            {'name': 'settings_register_1', 'on_enter': 'default_on_enter'},
            {'name': 'settings_register_3', 'on_enter': 'default_on_enter'},
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
                'conditions': 'default_is_proper', 'before': 'set_user_subscription'},
            {'trigger': 'back', 'source': 'settings_register_3', 'dest': 'idle'},
            # Title
            {'trigger': 'title', 'source': 'settings_menu', 'dest': 'settings_register_1'},
            {'trigger': 'message', 'source': 'settings_register_1', 'dest': 'idle',
                'conditions': 'default_is_proper', 'before': 'set_user_title'},
            {'trigger': 'back', 'source': 'settings_register_1', 'dest': 'idle'},
            # Delete
            {'trigger': 'delete', 'source': 'settings_menu', 'dest': 'settings_delete'},
            {'trigger': 'yesimsuredelete', 'source': 'settings_delete',
                'dest': 'unregistered', 'before': 'delete_user'},
            {'trigger': 'back', 'source': 'settings_delete', 'dest': 'idle'},
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
