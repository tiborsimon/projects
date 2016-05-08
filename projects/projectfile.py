import os
import re


class ProjectfileError(Exception):
    pass


_PROJECTFILE = 'Projectfile'
_VERSION_INDENTATION_ERROR = 'Whitespaces are not allowed before the "from" keyword!'
_VERSION_FORMAT_ERROR = 'Invalid version format. The valid one looks like "v1.2.3".'
_VERSION_MISSING_ERROR = 'You have to start your projectfile with the minimum supported version!'
_VARIABLE_INDENTATION_ERROR = 'Variables cannot be indented!'
_VARIABLE_QUOTE_BEFORE_ERROR = 'No matching quote found at the beginning of value!'
_VARIABLE_QUOTE_AFTER_ERROR = 'No matching quote found at the end of value!'
_COMMAND_HEADER_INDENTATION_ERROR = 'Command header cannot be indented!'
_COMMAND_HEADER_MISSING_COLON_ERROR = 'Missing colon after command name!'
_COMMAND_HEADER_COLON_ERROR = 'Invalid colon placement! It should be "command:".'
_COMMAND_HEADER_INVALID_ALTERNATIVE = 'Invalid command alternative syntax! It should be "command|c:".'
_COMMAND_HEADER_EMPTY_DEPENDENCY_LIST = 'Empty dependency list!'
_COMMAND_HEADER_INVALID_DEPENDENCY_LIST = 'Invalid dependency list syntax! It should be: "[dep1, dep2]".'


def _get_projectfile_list_for_project_root(project_root):
    result = []
    for root, dirs, files in os.walk(project_root):
        for name in files:
            if name == _PROJECTFILE:
                result.append(os.path.join(root, name))
    return result


def _load(path):
    with open(path, 'r') as f:
        raw = f.read()
    return raw.split('\n')


def _parse_version(line):
    m = re.match('^from\s+v?(\d+)\.(\d+)\.(\d+)\s*$', line)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        if re.match('^\s+from.*$', line):
            raise SyntaxError(_VERSION_INDENTATION_ERROR)
        elif re.match('^from.*$', line) and not re.match('^from\s+v?(\d+)\.(\d+)\.(\d+)\s*$', line):
            raise SyntaxError(_VERSION_FORMAT_ERROR)
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
    m = re.match('^(\w+)\s*=\s*(.*)$', line)
    if m:
        value = m.group(2).strip()
        temp_value = value
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                temp_value = value[1:]
            else:
                raise SyntaxError(_VARIABLE_QUOTE_AFTER_ERROR)
        if value.endswith('"') or value.endswith("'"):
            if value.startswith('"') or value.startswith("'"):
                value = temp_value[:-1]
            else:
                raise SyntaxError(_VARIABLE_QUOTE_BEFORE_ERROR)
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        return {m.group(1): value}
    else:
        if re.match('^\s+\w+\s*=\s*.*$', line):
            raise SyntaxError(_VARIABLE_INDENTATION_ERROR)
        return None


def _parse_command_divisor(line):
    if re.match('\s*===.*$', line):
        return True
    else:
        return False


def _parse_command_header(line):
    if re.match('^\s+.*', line):
        raise SyntaxError(_COMMAND_HEADER_INDENTATION_ERROR)
    m = re.match('^([\w\|\.\s-]+):\s*(?:\[([\w\.\s,-]+)\])?\s*$', line)
    if m:
        keys = m.group(1).split('|')
        keys = [k.strip() for k in keys]
        for key in keys:
            if not key:
                raise SyntaxError(_COMMAND_HEADER_INVALID_ALTERNATIVE)
        if m.group(2):
            deps = m.group(2).split(',')
            deps = [d.strip() for d in deps]
            for dep in deps:
                if not dep:
                    raise SyntaxError(_COMMAND_HEADER_INVALID_DEPENDENCY_LIST)
        else:
            deps = []

        ret = {
            keys[0]: {
                'dependencies': deps,
                'done': False
            }
        }
        if len(keys) > 1:
            for key in keys[1:]:
                ret[key] = {'alias': keys[0]}
        return ret
    else:
        if not re.search(':', line):
            raise SyntaxError(_COMMAND_HEADER_MISSING_COLON_ERROR)
        if re.search('(\w:\w|^:)', line):
            raise SyntaxError(_COMMAND_HEADER_COLON_ERROR)
        if re.search('\[\]', line):
            raise SyntaxError(_COMMAND_HEADER_EMPTY_DEPENDENCY_LIST)
        if re.search('[\[\]]', line):
            if not re.search('\[[^\[\]]*\]', line) or re.search('\[(\s*,\s*|[^,]*,\s*,[^,]*)\]', line):
                raise SyntaxError(_COMMAND_HEADER_INVALID_DEPENDENCY_LIST)
        return None


def _state_start(data, line):
    v = _parse_version(line)
    if v:
        data.update({'min-version': v})
        return _state_before_commands
    elif _parse_empty_line(line):
        return _state_start
    else:
        raise SyntaxError(_VERSION_MISSING_ERROR)


def _state_before_commands(data, line):
    if _parse_empty_line(line):
        return _state_before_commands
    if _parse_comment_delimiter(line):
        data.update({'description': {'done': False}})
        return _state_main_comment
    v = _parse_variable(line)
    if v:
        data.update({'variables': v})
        return _state_variables
    c = _parse_command_header(line)
    if c:
        data['commands'] = c
        return _state_command


def _state_main_comment():
    return None


def _state_variables():
    return None


def _state_command():
    return None