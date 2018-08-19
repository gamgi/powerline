from enum import Enum
from telegram import ReplyKeyboardMarkup, KeyboardButton


class MESSAGES_EN(Enum):
    START_HELLO_MESSAGE = "Hi, <description and some disclaimer>"
    #START_HELLO_MESSAGE = "Hi there. I'm a bot"
    REGISTER_1 = "What is your title?"
    REGISTER_2 = "What is your age?"
    REGISTER_3 = "How much would you like us to keep in touch?"


class MESSAGES_SE(Enum):
    START_HELLO_MESSAGE_SE = "Hej. Jag kanner en bot"
    REGISTER_1_SE = "Vad ar din tittel?"
    REGISTER_2_SE = "Vad ar din alder?"
    REGISTER_3_SE = "Hur mycket vill du hora av oss?"


MESSAGES = {'EN': MESSAGES_EN, 'SE': MESSAGES_SE}


class KEYBOARDS(Enum):
    REGISTER_1_KEYBOARD = ReplyKeyboardMarkup(
        [[KeyboardButton('mr'), KeyboardButton('mrs')]])
    REGISTER_2_KEYBOARD = ReplyKeyboardMarkup(
        [[KeyboardButton('1'), KeyboardButton('2')]])
    REGISTER_3_KEYBOARD = ReplyKeyboardMarkup(
        [[KeyboardButton('a little'), KeyboardButton('normal'), KeyboardButton('a lot')]])
