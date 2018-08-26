import logging
import logging
from transitions import Machine
from state_helpers import MachineHelpers

import enums
import state_register

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State(Machine, MachineHelpers, state_register.State):
    def __init__(self, bot):
        self.bot = bot
        self.language = 'EN'  # TODO
        states = [
            {'name': 'unregistered'},
            {'name': 'idle'},
            {'name': 'dummy_state'}]

        # Transitions
        transitions = [
            {'trigger': 'reset', 'source': '*', 'dest': 'unregistered'},
            {'trigger': 'dummy', 'source': '*', 'dest': 'dummy_state'}
        ]

        # Append to Machine
        self.transitions.append(transitions)
        self.states.append(states)

        Machine.__init__(
            self,
            states=self.states,
            transitions=self.transitions
            send_event=True,
            finalize_event=update_user_state
            initial='unregistered')

    """
    # Only for tests
    def update_user_state(self, event):
        # On successful transition, update user state
        if event.result:
            user = event.kwargs.get('user')
            assert user is not None
            user.state = event.transition.dest
    """
