import re

from projects.projectfile import error
from projects.projectfile.utils import get_current_command


def _run_state_machine(lines):
    data = {}
    state_function = _state_start
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
    _finish_processing(data, state_function)
    return data


def _parse_version(line):
    m = re.match('^from\s+v?(\d+)\.(\d+)\.(\d+)\s*$', line)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        if re.match('^\s+from.*$', line):
            raise SyntaxError(error.VERSION_INDENTATION_ERROR)
        elif re.match('^from.*$', line) and not re.match('^from\s+v?(\d+)\.(\d+)\.(\d+)\s*$', line):
            raise SyntaxError(error.VERSION_FORMAT_ERROR)
        else:
            return None


def _parse_line(line):
    m = re.match('^(.*)$', line)
    if m:
        return m.group(1).strip()
    else:
        return None


def _parse_empty_line(line):
    if re.match('^\s*$', line):
        return True
    else:
        return False


def _parse_indented_line(line):
    m = re.match('^\s+(.*)$', line)
    if m:
        return m.group(1).strip()
    else:
        return None


def _parse_comment_delimiter(line):
    if re.match('\s*""".*$', line):
        return True
    else:
        return False


def _parse_variable(line):
    m = re.match('^([\w\.-]+)\s*=\s*(.*)$', line)
    if m:
        value = m.group(2).strip()
        temp_value = value
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                temp_value = value[1:]
            else:
                raise SyntaxError(error.VARIABLE_QUOTE_AFTER_ERROR)
        if value.endswith('"') or value.endswith("'"):
            if value.startswith('"') or value.startswith("'"):
                value = temp_value[:-1]
            else:
                raise SyntaxError(error.VARIABLE_QUOTE_BEFORE_ERROR)
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        return {m.group(1): value}
    else:
        if re.match('^\s+[\w\.-]+\s*=\s*.*$', line):
            raise SyntaxError(error.VARIABLE_INDENTATION_ERROR)
        return None


def _parse_command_divisor(line):
    if re.match('\s*===.*$', line):
        return True
    else:
        return False


def _parse_command_header(line):
    if re.match('^\s+.*:.*', line):
        raise SyntaxError(error.COMMAND_HEADER_INDENTATION_ERROR)
    m = re.match('^([\w\|\.\s-]+):\s*(?:\[([\w\.\s,-]+)\])?\s*$', line)
    if m:
        keys = m.group(1).split('|')
        keys = [k.strip() for k in keys]
        for key in keys:
            if not key:
                raise SyntaxError(error.COMMAND_HEADER_INVALID_ALTERNATIVE)
        if m.group(2):
            deps = m.group(2).split(',')
            deps = [d.strip() for d in deps]
            for dep in deps:
                if not dep:
                    raise SyntaxError(error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)
        else:
            deps = []

        ret = {keys[0]: {'done': False}}
        if deps:
            ret[keys[0]]['dependencies'] = deps
        if len(keys) > 1:
            for key in keys[1:]:
                ret[key] = {'alias': keys[0]}
        return ret
    else:
        if not re.match('^\s+.*', line) and not re.search(':', line):
            raise SyntaxError(error.COMMAND_HEADER_MISSING_COLON_ERROR)
        if not re.match('^\s+.*', line) and re.search('(\w:\w|^:)', line):
            raise SyntaxError(error.COMMAND_HEADER_COLON_ERROR)
        if re.search('\[\]', line):
            raise SyntaxError(error.COMMAND_HEADER_EMPTY_DEPENDENCY_LIST)
        if re.search('[\[\]]', line):
            if not re.search('\[[^\[\]]*\]', line) or re.search('\[(\s*,\s*|[^,]*,\s*,[^,]*)\]', line):
                raise SyntaxError(error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)
        raise SyntaxError(error.COMMAND_HEADER_SYNTAX_ERROR)


def _state_start(data, line):
    v = _parse_version(line)
    if v:
        data.update({'min-version': v})
        return _state_before_commands
    elif _parse_empty_line(line):
        return _state_start
    else:
        raise SyntaxError(error.VERSION_MISSING_ERROR)


def _state_before_commands(data, line):
    if _parse_empty_line(line):
        return _state_before_commands
    if _parse_comment_delimiter(line):
        return _state_main_comment
    v = _parse_variable(line)
    if v:
        data.update({'variables': v})
        return _state_variables
    c = _parse_command_header(line)
    if c:
        data['commands'] = c
        return _state_command
    else:
        raise SyntaxError(error.COMMAND_HEADER_SYNTAX_ERROR)


def _state_main_comment(data, line):
    if _parse_comment_delimiter(line):
        return _state_variables
    if 'description' not in data:
        data['description'] = ''
    l = _parse_line(line)
    if l:
        if data['description'] == '':
            data['description'] = l
        else:
            if data['description'][-2:] != '\n\n':
                data['description'] += ' ' + l
            else:
                data['description'] += l
        return _state_main_comment
    if _parse_empty_line(line):
        if data['description'] != '':
            if data['description'][-2:] != '\n\n':
                data['description'] += '\n\n'
        return _state_main_comment


def _state_variables(data, line):
    if _parse_empty_line(line):
        return _state_variables
    if _parse_comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    v = _parse_variable(line)
    if v:
        if 'variables' not in data:
            data['variables'] = {}
        data['variables'].update(v)
        return _state_variables
    else:
        c = _parse_command_header(line)
        if c:
            data['commands'] = c
            return _state_command
        else:
            raise SyntaxError(error.VARIABLE_SYNTAX_ERROR)


def _state_command(data, line):
    if _parse_empty_line(line):
        return _state_command
    current_command = get_current_command(data)
    if _parse_comment_delimiter(line):
        return _state_command_comment
    if _parse_command_divisor(line):
        return _state_post
    l = _parse_indented_line(line)
    if l:
        current_command['pre'] = [l]
        return _state_pre
    else:
        raise SyntaxError(error.COMMAND_HEADER_UNEXPECTED_UNINDENTED_ERROR)


def _state_command_comment(data, line):
    if _parse_comment_delimiter(line):
        return _state_pre
    current_command = get_current_command(data)
    if 'description' not in current_command:
        current_command['description'] = ''
    l = _parse_line(line)
    if l:
        if current_command['description'] == '':
            current_command['description'] = l
        else:
            if current_command['description'][-2:] != '\n\n':
                current_command['description'] += ' ' + l
            else:
                current_command['description'] += l
        return _state_command_comment
    if _parse_empty_line(line):
        if current_command['description'] != '':
            if current_command['description'][-2:] != '\n\n':
                current_command['description'] += '\n\n'
        return _state_command_comment


def _state_pre(data, line):
    if _parse_empty_line(line):
        return _state_pre
    if _parse_comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    current_command = get_current_command(data)
    if 'pre' not in current_command:
        current_command['pre'] = []
    if _parse_command_divisor(line):
        return _state_post
    l = _parse_indented_line(line)
    if l:
        current_command['pre'].append(l)
        return _state_pre
    c = _parse_command_header(line)
    if c:
        current_command['done'] = True
        data['commands'].update(c)
        return _state_command


def _state_post(data, line):
    if _parse_empty_line(line):
        return _state_post
    if _parse_command_divisor(line):
        raise SyntaxError(error.COMMAND_DELIMITER_UNEXPECTED_ERROR)
    if _parse_comment_delimiter(line):
        raise SyntaxError(error.COMMENT_DELIMITER_UNEXPECTED_ERROR)
    current_command = get_current_command(data)
    if 'post' not in current_command:
        current_command['post'] = []
    l = _parse_indented_line(line)
    if l:
        current_command['post'].append(l)
        return _state_post
    c = _parse_command_header(line)
    if c:
        current_command['done'] = True
        data['commands'].update(c)
        return _state_command


def _finish_processing(data, state):
    if state in (_state_pre, _state_post):
        for command_name in data['commands']:
            if 'done' in data['commands'][command_name]:
                del data['commands'][command_name]['done']
    elif state == _state_start:
        raise SyntaxError(error.PROJECTFILE_EMPTY_ERROR)
    elif state in (_state_before_commands, _state_variables, _state_main_comment):
        raise SyntaxError(error.PROJECTFILE_NO_COMMAND_ERROR)
    elif state in (_state_command, _state_command_comment):
        for command in data['commands']:
            if not data['commands'][command]['done']:
                break
        raise SyntaxError(error.PROJECTFILE_NO_COMMAND_IN_COMMAND_ERROR.format(command))






