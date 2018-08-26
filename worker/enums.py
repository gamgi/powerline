from telegram import ReplyKeyboardMarkup, KeyboardButton


MESSAGES_EN = dict(
    START_HELLO_MESSAGE="Hi, <description and some disclaimer>",
    REGISTER_1="What is your title?",
    REGISTER_2="What is your age?",
    REGISTER_3="How much would you like us to keep in touch?",
    REGISTER_3_EXIT="Thanks! We'll be in touch. Don't hesitate to message us."
)

MESSAGES_SE = dict(
    START_HELLO_MESSAGE_SE="Hej. Jag kanner en bot",
    REGISTER_1="Vad ar din tittel?",
    REGISTER_2="Vad ar din alder?",
    REGISTER_3="Hur mycket vill du hora av oss?",
    REGISTER_3_EXIT="Tack! Vi hör av oss snart.. Vi vill gärna veta om du har något att tala om."
)

MESSAGES = {'EN': MESSAGES_EN, 'SE': MESSAGES_SE}


KEYBOARDS = dict(
    REGISTER_1=ReplyKeyboardMarkup(
        [[KeyboardButton('mr'), KeyboardButton('mrs')]],
        one_time_keyboard=True),
    REGISTER_2=ReplyKeyboardMarkup(
        [[KeyboardButton('1'), KeyboardButton('2')]],
        one_time_keyboard=True),
    REGISTER_3=ReplyKeyboardMarkup(
        [[KeyboardButton('a little'), KeyboardButton(
            'normal'), KeyboardButton('a lot')]],
        one_time_keyboard=True)
)
