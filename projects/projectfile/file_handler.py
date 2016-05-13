import os


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