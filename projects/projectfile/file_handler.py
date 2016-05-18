import os
from os import walk
from . import defs
from . import error


def get_file_content(file_path):
    pass


def projectfile_walk(project_root):
    result = []
    for root, dirs, files in walk(project_root):
        w = []
        for f in files:
            if f == defs.PROJECTFILE:
                w.append(root)
                path = os.path.join(root, f)
                w.append(_load(path))
                result.append(tuple(w))
    if not result:
        raise error.ProjectfileError({
            'error': error.PROJECTFILE_NO_PROJECTFILE
        })
    return result


def _load(path):
    with open(path, 'r') as f:
        raw = f.read()
    return raw.split('\n')
