import logging
from redis import StrictRedis
from transitions import Machine

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class State(Machine):
    # self.is_waiting_message=True
    # def save_to_db
    def on_enter_register_1(self, event):
        chat_id = event.kwargs.get('chat_id')
        self.bot.send_message(chat_id=chat_id,
                              text="Najs")

    def __init__(self, bot):
        self.bot = bot
        states = [
            'unregistered',
            'register_1',
            'register_2',
            'register_3',
            'idle',
            'dummy_state']

        commands = [
            {'trigger': 'start', 'source': 'unregistered', 'dest': 'register_1'},
            {'trigger': 'dummy', 'source': '*', 'dest': 'dummy_state'}
        ]
        transitions = [
            {'trigger': 'ask_a', 'source': 'unregistered', 'dest': 'register_1'},
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
