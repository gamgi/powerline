import logging
from transitions import Machine
from state_helpers import MachineHelpers

import enums
import state_register
import state_settings

# Logging state transitions for debugging
# logging.getLogger('transitions').setLevel(logging.INFO)


class State(Machine, MachineHelpers, state_register.State, state_settings.State):
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
            {'trigger': 'dummy', 'source': '*', 'dest': 'dummy_state'},
            {'trigger': 'admin', 'source': '*', 'dest': 'admin_state'}
        ]

        # Append to Machine
        self.machine_add_states_and_transitions(states, transitions)

        Machine.__init__(
            self,
            states=self.states,
            transitions=self.transitions,
            send_event=True,
            finalize_event=self.update_user_state,
            initial='unregistered')

    # Only for tests. State is normally saved at end of "last" transition in worker.py.
    # For inspecting we need to save in-between
    def update_user_state(self, event):
        # On successful transition, update user state
        if event.result:
            user = event.kwargs.get('user')
            assert user is not None
            user.state = event.transition.dest
