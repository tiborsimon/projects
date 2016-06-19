from subprocess import call
import os
from projects import config
from projects import paths
from projects import projectfile
import gui
from subprocess import call
import re


return_path = ''


def path_setting_callback(path):
    global return_path
    return_path = path


def execute(args, data):
    if len(args) > 2:
        args = args[2:]
        for command_name in args:
            if command_name in data['commands']:
                command = data['commands'][command_name]
                if 'alias' in command:
                    command = data['commands'][command['alias']]
                for lines in command['script']:
                    call(re.sub('\s+', ' ', lines).split(' '))
            else:
                pass
                # no command..

def main(args):
    try:
        conf = config.get()
        if paths.inside_project(conf['projects-path']):
            project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
            data = projectfile.get_data_for_root(project_root)
            execute(args, data)

        else:
            # start project selection
            gui.select_project(
                paths.list_dir_for_path(conf['projects-path']),
                path_setting_callback
            )
            if return_path:
                with open(os.path.join(os.path.expanduser('~'), '.p-path'), 'w+') as f:
                    f.write(os.path.join(os.path.expanduser(conf['projects-path']), return_path))

    except Exception as e:
        print(e)
        pass
