import os
import sys
from projects import config
from projects import paths
from projects import projectfile
from projects.projectfile.error import ProjectfileError
import gui
from subprocess import call
import re
from termcolor import colored


return_path = ''


def path_setting_callback(path):
    global return_path
    return_path = path


def process_command(command_name, data):
    command = data['commands'][command_name]
    if 'alias' in command:
        command = data['commands'][command['alias']]
    if 'dependencies' in command:
        for dep in command['dependencies']:
            process_command(dep, data)
    for lines in command['script']:
        call(re.sub('\s+', ' ', lines).split(' '))


def execute(args, data):
    if len(args) > 2:
        args = args[2:]
        for command_name in args:
            if command_name in data['commands']:
                process_command(command_name, data)
            else:
                pass
                # no command found
    else:
        # show gui for project
        gui.show_project_details(data, 80)


def main(args):
    try:
        conf = config.get()
        if paths.inside_project(conf['projects-path']):
            project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
            data = projectfile.get_data_for_root(project_root['path'])
            data['name'] = project_root['name']
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

    except ProjectfileError as e:
        error = e.args[0]
        message = '\n Projectfile error!\n {}'.format(error['error'])
        if 'path' in error:
            message = '{}\n Path: {}/Projectfile'.format(message, error['path'])
        if 'line' in error:
            message = '{}\n Line: {}'.format(message, error['line'])
        print(colored(message, 'red'))
        sys.exit(-1)

