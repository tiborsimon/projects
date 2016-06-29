from . import parse
from .. import error
from .. import utils


def start(data, line):
    v = parse.version(line)
    if v:
        data.update({'min-version': v})
        return before_commands
    elif parse.empty_line(line):
        return start
    else:
        raise SyntaxError(error.VERSION_MISSING_ERROR)


def before_commands(data, line):
    if parse.empty_line(line):
        return before_commands
    if parse.comment_delimiter(line):
        return main_comment
    v = parse.variable(line)
    if v:
        data.update({'variables': v})
        return variables
    c = parse.command_header(line)
    if c:
        data['commands'] = c
        return command
    else:
        raise SyntaxError(error.COMMAND_HEADER_SYNTAX_ERROR)


def main_comment(data, line):
    if parse.comment_delimiter(line):
        return variables
    if 'description' not in data:
        data['description'] = ''
    l = parse.line(line)
    if l:
        if data['description'] == '':
            data['description'] = l
        else:
            if data['description'][-2:] != '\n\n':
                data['description'] += ' ' + l
            else:
                data['description'] += l
        return main_comment
    if parse.empty_line(line):
        if data['description'] != '':
            if data['description'][-2:] != '\n\n':
                data['description'] += '\n\n'
        return main_comment


def variables(data, line):
    if parse.empty_line(line):
        return variables
    if parse.comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    v = parse.variable(line)
    if v:
        if 'variables' not in data:
            data['variables'] = {}
        data['variables'].update(v)
        return variables
    else:
        c = parse.command_header(line)
        if c:
            data['commands'] = c
            return command
        else:
            raise SyntaxError(error.VARIABLE_SYNTAX_ERROR)


def command(data, line):
    if parse.empty_line(line):
        return command
    current_command = utils.get_current_command(data)
    if parse.comment_delimiter(line):
        return command_comment
    if parse.command_divisor(line):
        return post
    l = parse.indented_line(line)
    if l:
        current_command['pre'] = [l]
        return pre
    else:
        raise SyntaxError(error.COMMAND_HEADER_UNEXPECTED_UNINDENTED_ERROR)


def command_comment(data, line):
    if parse.comment_delimiter(line):
        return pre
    current_command = utils.get_current_command(data)
    if 'description' not in current_command:
        current_command['description'] = ''
    l = parse.line(line)
    if l:
        if current_command['description'] == '':
            current_command['description'] = l
        else:
            if current_command['description'][-2:] != '\n\n':
                current_command['description'] += ' ' + l
            else:
                current_command['description'] += l
        return command_comment
    if parse.empty_line(line):
        if current_command['description'] != '':
            if current_command['description'][-2:] != '\n\n':
                current_command['description'] += '\n\n'
        return command_comment


def pre(data, line):
    if parse.empty_line(line):
        return pre
    if parse.comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    current_command = utils.get_current_command(data)
    if 'pre' not in current_command:
        current_command['pre'] = []
    if parse.command_divisor(line):
        return post
    l = parse.indented_line(line)
    if l:
        current_command['pre'].append(l)
        return pre
    c = parse.command_header(line)
    if c:
        current_command['done'] = True
        utils.assert_command_is_present(c, data)
        data['commands'].update(c)
        return command


def post(data, line):
    if parse.empty_line(line):
        return post
    if parse.command_divisor(line):
        raise SyntaxError(error.COMMAND_DELIMITER_UNEXPECTED_ERROR)
    if parse.comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    current_command = utils.get_current_command(data)
    if 'post' not in current_command:
        current_command['post'] = []
    l = parse.indented_line(line)
    if l:
        current_command['post'].append(l)
        return post
    c = parse.command_header(line)
    if c:
        current_command['done'] = True
        utils.assert_command_is_present(c, data)
        data['commands'].update(c)
        return command
