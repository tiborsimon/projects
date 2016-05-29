from .. import error
from . import state


def process_lines(lines):
    data = _parse_lines(lines)
    _data_integrity_check(data)
    return data


def _parse_lines(lines):
    data = {}
    state_function = state.start
    for i in range(len(lines)):
        try:
            state_function = state_function(data, lines[i])
        except SyntaxError as e:
            message = e.args[0]
            raise error.ProjectfileError({
                'line': i + 1,
                'error': message
            })
    _finish_processing(data, state_function)
    return data


def _finish_processing(data, st):
    if st in (state.pre, state.post):
        for command_name in data['commands']:
            if 'done' in data['commands'][command_name]:
                del data['commands'][command_name]['done']
    elif st == state.start:
        raise SyntaxError(error.PROJECTFILE_EMPTY_ERROR)
    elif st in (state.before_commands, state.variables, state.main_comment):
        raise SyntaxError(error.PROJECTFILE_NO_COMMAND_ERROR)
    elif st in (state.command, state.command_comment):
        for c in data['commands']:
            if not data['commands'][c]['done']:
                break
        raise SyntaxError(error.PROJECTFILE_NO_COMMAND_IN_COMMAND_ERROR.format(c))


def _data_integrity_check(data):
    """Checks if all command dependencies refers to and existing command. If not, a ProjectfileError
    will be raised with the problematic dependency and it's command.

    :param data: parsed raw data set.
    :return: None
    """
    deps = []
    for command in data['commands']:
        if 'dependencies' in data['commands'][command]:
            for d in data['commands'][command]['dependencies']:
                deps.append({
                    'd': d,
                    'c': command
                })
    for d in deps:
        if d['d'] not in data['commands']:
            raise error.ProjectfileError({
                'error': error.PROJECTFILE_INVALID_DEPENDENCY.format(d['d'], d['c'])
            })
