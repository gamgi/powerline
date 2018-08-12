import logging
from redis import StrictRedis
from transitions import Machine
# The states
states = ['unregistered', 'register_1', 'register_2', 'register_3', 'idle']

# Transitions between states
transitions = [
    {'trigger': 'asa_a', 'source': 'unregistered', 'dest': 'register_1'},
    {'trigger': 'ask_b', 'source': 'register_1', 'dest': 'register_2'},
    {'trigger': 'ask_c', 'source': 'register_2', 'dest': 'register_3'},
    {'trigger': 'complete_register', 'source': 'register_3', 'dest': 'idle'},
]

# Initialize state machine
machine = Machine(
    states=states,
    transitions=transitions,
    initial='unregistered')

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)

# User class
users = []


class User(object):
    def __init__(self):
        users.append(self)
        machine.add_model(user)
