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


def _parse(lines):
    ret = {}

    version_found = 0
    p_version = re.compile('^from\s+v?(\d+).(\d+).(\d+)\s*$')
    p_invalid_version = re.compile('^\s+from')

    for index in range(len(lines)):
        m = p_version.match(lines[index])
        if m:
            ret['min-version'] = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            version_found = 1
        m = p_invalid_version.match(lines[index])
        if m:
            raise ProjectfileError('Syntax error in line {}: '
                                   'Whitespaces are not allowed before the "from" keyword!'.format(index+1))
    else:
        if not version_found:
            raise ProjectfileError('Syntax error: Mandatory minimum version (from vx.x.x) is missing! '
                                   'That should be the first thing you define in your Projectfile.')

    return ret



