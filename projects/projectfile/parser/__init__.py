from .. import error
from . import state


def finish_processing(data, st):
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


def process_lines(lines):
    data = {}
    state_function = state.start
    for i in range(len(lines)):
        try:
            state_function = state_function(data, lines[i])
        except SyntaxError as e:
            try:
                msg = e.message
            except AttributeError:
                msg = e.msg
            raise error.ProjectfileError({
                'line': i + 1,
                'error': msg
            })
    finish_processing(data, state_function)
    return data