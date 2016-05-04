import os
import re


class ProjectfileError(Exception):
    pass


def _get_projectfile_list_for_project_root(project_root):
    result = []
    for root, dirs, files in os.walk(project_root):
        for name in files:
            if name == 'Projectfile':
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
        raise SyntaxError('Whitespaces are not allowed before the "from" keyword!')
    if not re.match('.*v?\d+.\d+.\d+.*', line):
        raise SyntaxError('Invalid version format. The valid one looks like "v1.2.3".')
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
