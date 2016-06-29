from . import error

def get_current_command(data):
    for command in data['commands']:
        if 'done' in data['commands'][command]:
            if not data['commands'][command]['done']:
                return data['commands'][command]
    else:
        return None


def assert_command_is_present(c, data):
    for key in c:
        if key in data['commands']:
            raise SyntaxError(error.COMMAND_HEADER_REDEFINED_ERROR.format(key))
