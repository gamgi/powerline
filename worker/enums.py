from enum import Enum


class MessagesEN(Enum):
    START_HELLO_MESSAGE = "Moro, <joku disclaiemr tähän>"
    #START_HELLO_MESSAGE = "Hi there. I'm a bot"
    REGISTER_A = "What is your A?"


class MessagesSE(Enum):
    START_HELLO_MESSAGE_SE = "Hej. Jag kanner en bot"
    REGISTER_A_SE = "Vad ar ditt A?"


MESSAGES = {'EN': MessagesEN, 'SE': MessagesSE}
