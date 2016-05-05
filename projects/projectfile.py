import os
import re


class ProjectfileError(Exception):
    pass


_PROJECTFILE = 'Projectfile'
_VERSION_INDENTATION_ERROR = 'Whitespaces are not allowed before the "from" keyword!'
_VERSION_FORMAT_ERROR = 'Invalid version format. The valid one looks like "v1.2.3".'
_VARIABLE_INDENTATION_ERROR = 'Variables cannot be indented!'
_VARIABLE_QUOTE_BEFORE_ERROR = 'No matching quote found at the beginning of value!'
_VARIABLE_QUOTE_AFTER_ERROR = 'No matching quote found at the end of value!'


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


def _valid_version(line):
    m = re.match('^from\s+v?(\d+).(\d+).(\d+)\s*$', line)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        return None


def _invalid_version(line):
    if re.match('^\s+from/*', line):
        raise SyntaxError(_VERSION_INDENTATION_ERROR)
    if not re.match('.*v?\d+.\d+.\d+.*', line):
        raise SyntaxError(_VERSION_FORMAT_ERROR)
    return None


def _line(line):
    m = re.match('^(.*)$', line)
    if m:
        return m.group(1).strip()
    else:
        return None


def _empty_line(line):
    if re.match('^\s*$', line):
        return True
    else:
        return False


def _indented_line(line):
    m = re.match('^\s+(.*)$', line)
    if m:
        return m.group(1).strip()
    else:
        return None


def _comment_delimiter(line):
    if re.match('\s*""".*$', line):
        return True
    else:
        return False


def _valid_variable(line):
    m = re.match('^(\w+)\s*=\s*(.*)$', line)
    if m:
        value = m.group(2).strip()
        temp_value = value
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                temp_value = value[1:]
            else:
                return None
        if value.endswith('"') or value.endswith("'"):
            if value.startswith('"') or value.startswith("'"):
                value = temp_value[:-1]
            else:
                return None
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        return {m.group(1): value}
    else:
        return None


def _invalid_variable(line):
    if re.match('^\s+\w+\s*=\s*.*$', line):
        raise SyntaxError(_VARIABLE_INDENTATION_ERROR)
    m = re.match('^(\w+)\s*=\s*(.*)$', line)
    if m:
        value = m.group(2).strip()
        temp_value = value
        if value.startswith('"') or value.startswith("'"):
            if value.endswith('"') or value.endswith("'"):
                pass
            else:
                raise SyntaxError(_VARIABLE_QUOTE_AFTER_ERROR)
        if value.endswith('"') or value.endswith("'"):
            if value.startswith('"') or value.startswith("'"):
                pass
            else:
                raise SyntaxError(_VARIABLE_QUOTE_BEFORE_ERROR)
    return None


def _command_divisor(line):
    if re.match('\s*===.*$', line):
        return True
    else:
        return False
