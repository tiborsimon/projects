import os
import sys
from projects import config
from projects import paths
from projects import projectfile
import gui
import subprocess
from termcolor import colored
import pydoc


__version__ = '1.0.0'

help_text = """\
===============================================================================
                                      _           _
                                     (_)         | |
                      _ __  _ __ ___  _  ___  ___| |_ ___
                     | '_ \| '__/ _ \| |/ _ \/ __| __/ __|
                     | |_) | | | (_) | |  __/ (__| |_\__ \\
                     | .__/|_|  \___/| |\___|\___|\__|___/
                     | |            _/ |
                     |_|           |__/

===============================================================================
            i n t u i t i v e   p r o j e c t   m a n a g e m e n t
===============================================================================

 Features
     - quick project navigation
     - Projectfile based recursive scripting system
     - instant help menu generation

 Usage:
     p
     p p
     p <command>
     p [-h|--help]
     p [-v|--version]
     p [-i|--init]

 Terms:
     Project directory - the directory where you store all your projects. Inside
                         this directory are your root directories of your
                         projects repositories.
     Projectfile - the file you write to projects

 p
     This command is the main trigger for projects. It behaves differently
     depending on your current working directory.

     OUTSIDE your projects directory, it opens the project
     selector screen, where you can



"""

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
    for line in command['script']:
        err, out = execute_call(line)
        if out:
            print(out.strip())
        if err:
            print(colored(err.strip(), 'red'))


def execute_call(line):
    process = subprocess.Popen(line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return err, out


def execute(args, data, conf):
    if args:
        for command_name in args:
            if command_name in data['commands']:
                process_command(command_name, data)
            else:
                pass
    else:
        gui.show_project_details(data, conf['doc-width'])


def main(args):
    try:
        conf = config.get()
        args = args[2:]
        if len(args) == 1:
            if args[0] in ['-v', '--version']:
                print(__version__)
                return
            elif args[0] in ['-i', '--init']:
                if os.path.isfile('Projectfile'):
                    print('You already have a Projectfile in this directory.. Nothing to do ;)')
                else:
                    projectfile_content = projectfile.DEFAULT_PROJECTFILE.format(__version__)
                    with open('Projectfile', 'w+') as f:
                        f.write(projectfile_content)
                    print('Projectfile created.')
                return
            elif args[0] in ['-h', '--help']:
                pydoc.pager(help_text)
                return
            elif args[0] in ['p']:
                handle_project_selection(conf)
                return

        if paths.inside_project(conf['projects-path']):
            handle_inside_project(args, conf)
        else:
            handle_project_selection(conf)

    except projectfile.error.ProjectfileError as e:
        error = e.args[0]
        message = '\n Projectfile error!\n {}'.format(error['error'])
        if 'path' in error:
            message = '{}\n Path: {}/Projectfile'.format(message, error['path'])
        if 'line' in error:
            message = '{}\n Line: {}'.format(message, error['line'])
        print(colored(message, 'red'))
        sys.exit(-1)

    except config.ConfigError as e:
        error = e.args[0]
        message = '\n Config error!\n {}'.format(error)
        print(colored(message, 'red'))
        sys.exit(-1)


def handle_project_selection(conf):
    gui.select_project(
        paths.list_dir_for_path(conf['projects-path']),
        path_setting_callback
    )
    if return_path:
        with open(os.path.join(os.path.expanduser('~'), '.p-path'), 'w+') as f:
            f.write(os.path.join(os.path.expanduser(conf['projects-path']), return_path))


def handle_inside_project(args, conf):
    project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
    data = projectfile.get_data_for_root(project_root['path'])
    data['name'] = project_root['name']
    execute(args, data, conf)

