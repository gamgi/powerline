def get_command_from_update(update):
    try:
        message = update.message.text
        if (not message.startswith('/')):
            return None
        message = message.replace('/', '', 1)
        return message.partition(' ')[0]
    except BaseException:
        return None


def get_command_and_args_from_update(update):
    try:
        message = update.message.text
        if (not message.startswith('/')):
            return None, None
        if ' ' not in update.message.text:
            command = get_command_from_update(update)
            return command, []
        command, unused, args_joined = update['message']['text'].partition(' ')
        return command.replace('/', '', 1), args_joined.split(' ')
    except BaseException as err:
        logging.info(err)
        return None


def get_user_id_from_update(update):
    try:
        # Note: from is a reserved word, so key is in python "from_user"
        return update.message.from_user.id
        # return update.message.from_user.id
    except BaseException:
        return None

    return ''


def get_message_from_update(update):
    try:
        return update.message.text
    except BaseException:
        return None
