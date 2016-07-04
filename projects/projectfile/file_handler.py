import os
from os import walk
from . import defs
from . import error
from projects.projectfile import parser


def get_walk_data(root):
    return walk(root)


def get_node_list(project_root):
    result = []
    for root, dirs, files in get_walk_data(project_root):
        for f in files:
            if f == defs.PROJECTFILE:
                try:
                    raw_lines = _load(os.path.join(root, f))
                    node = {'path': root}
                    node.update(parser.process_lines(raw_lines))
                    result.append(node)
                except Exception as e:
                    message = e.args[0]
                    message['path'] = root
                    raise error.ProjectfileError(message)
    if not result:
        raise error.ProjectfileError({
            'error': error.PROJECTFILE_NO_PROJECTFILE
        })
    return result


def _load(path):
    with open(path, 'r') as f:
        raw = f.read()
    return raw.split('\n')
