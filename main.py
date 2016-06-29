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

 Features:
     - quick project navigation
     - Projectfile based recursive scripting system
     - instant help menu generation


 Usage:
     p
     p -p
     p <command>
     p [-h|--help]
     p [-v|--version]
     p [-i|--init]
     p [-w|--walk]


 Terminology:
     Project directory
         The directory where you store all your projects. Inside this directory
         are your root directories of your project repositories. You can define
         your project root directory in the ~/.prc configuration file with the
         "projects-path" keyword. The default root is "~/projects".

     Projectfile
         The file you write to tell <projects> what to do. You can place a
         Projectfile into every directory you have in your project. <projects>
         will recursively process them in alphabetical walk order.

     Command
         Command you define in at least one of the Projectfiles. If you define
         a command in multiple Projectfiles, the commands will be appended
         according to the alphabetical walk order. You can execute this command
         with the given keywords. There is a possibility to split the execution
         of an outer command body and execute the it's children's command bodies.
         See the Projectfile section for more details.

     Alternative
         You can give alternative keywords for a command. These alternatives
         usually a shorter versions of the original keyword to speed up the
         typing.

     Dependencies
         You can add dependencies to a command that will be executed before the
         actual command will be executed. The dependency list is an ordered list
         of other command keywords or alternatives.


 p

     This command is the main trigger for projects. It behaves differently
     depending on your current working directory.

     OUTSIDE your projects directory, it opens the project selector screen,
     where you can select your project by typing the projects name or by using
     the arrows keys.

     INSIDE any of your projects (inside the repository root directory) this
     command will show the manual generated from the Projectfiles.


 p -p

     This command behaves the same as the previous "p" command but it will
     always display the project selector screen. This could be handy if you want
     to switch projects quickly.


 p <command>

     This is the command for executing commands defined in the Projectfiles. By
     convention all defined command should start with an alphanumeric character.
     The commands started with a dash reserved for <projects> itself.


 p [-h|--help]

     Brings up this help screen.


 p [-v|--version]

     Prints out the current <projects> version.


 p [-i|--init]

     Generates a template Projectfile into the current directory.


 p [-w|--walk]

     List out all directories in your project in the walk order <projects>
     will follow. It marks the directories that contain a Projectfile.


===============================================================================
                 _____           _           _    __ _ _
                |  __ \         (_)         | |  / _(_) |
                | |__) | __ ___  _  ___  ___| |_| |_ _| | ___
                |  ___/ '__/ _ \| |/ _ \/ __| __|  _| | |/ _ \\
                | |   | | | (_) | |  __/ (__| |_| | | | |  __/
                |_|   |_|  \___/| |\___|\___|\__|_| |_|_|\___|
                               _/ |
                              |__/
===============================================================================

 Projectfiles are the files you create in order to define commands that will
 be executed with the "p <command>". Projectfiles provide a powerful and self
 explanatory way to interact with your project.

 You can create an example Projectfile with the "p [-i|--init]" command. The
 generated Projectfile will demonstrate all provided functionality except the
 recursive command concatenation since it will generate only one Projectfile.

-------------------------- Projectfile format ---------------------------------

 There are mandatory and optional features you can add to Projectfile.

 Mandatory:
    - <projects> version
    - at least one command definition header
    - command body

 Optional:
    - main description
    - variables
    - command alternatives
    - command dependency list
    - command description
    - recursive separator

 There is a strict order where you can place each features. Between each
 feature arbitrary number of empty lines are allowed. The order is the
 following:

    1. <projects> version
    2. main description
    3. variables
    4. command header
    5. command description
    6. command pre-body
    7. recursive separator
    8. command post-body


 <projects> version [mandatory]

    '''
    from v1.0.0
    '''

    This feature will define the earliest version that is compatible with the
    used Projectfile format. All <projects> versions greater or equal to the
    defined one will be compatible with the format, but earlier versions may
    have problems with future features. The first release version is v1.0.0.


 main description [optional]

    '''
    \"\"\"
    A description for the project..
    \"\"\"
    '''

    After the version you can define a global description of the whole project.
    You can write long lines, <projects> will wrap them according to the defined
    "doc-width" key in the ~/.prc configuration file. Single line breaks won't
    break the lines in the generated manual. You have to use an empty line in
    order to add a line break.

    If you have multiple Projectfiles created, the main descriptions will be
    concatenated with empty lines according to the walk order.


 variables [optional]

    '''
    variable = 42
    other_variable = "This is a string with spaces"
    yet_another_variable = Quotes are optional. This is still valid.
    '''

    You can define variables as well. Each variable will be used as a string. No
    other variable format is currently supported. You can omit the quotes if you
    want, <projects> will use the entire string you write after the "=" sign.

    To use the variables you need to escape them:

        $variable
        ${variable}

    Both escapement is interpreted equally.

    Defined variables go to the global variable pool. You cannot assign a
    variable the more than once. Hence you cannot redefine a variable in a later
    Projectfile (a Projectfile is thant is processed later according to the walk
    order). Redefining a variable will raise an error. Since every variables go
    to the global variable pool, you can use the variables in any Projectfile
    independently which Projectfile you defined them. It is possible to use a
    variable in the root level Projectfile that is defined in a later Projectfile.


 command header [mandatory]

    '''
    my_command|alternative1|alt2: [dependency1, dependency2]
    '''

    The command header feature allows you to define a command, it's alternatives
    and it's dependent other commands. The first keyword is the default keyword
    for the command. Alternatives are separated with the pipe "|" character.
    After the keyword definitions, a colon ":" closes the command header. After
    the colon, you can define a list of other commands, that are executed in
    the order you defined them before the current command execution.

    A command cannot be redefined in the same Projectfile twice. If you redefine
    a command in another Projectfile, the commands' body will be appended to
    each other according to the path relationship of these files.  



 Recursive command concatenation





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
                if paths.inside_project(conf['projects-path']):
                    if os.path.isfile('Projectfile'):
                        print('You already have a Projectfile in this directory.. Nothing to do ;)')
                    else:
                        projectfile_content = projectfile.DEFAULT_PROJECTFILE.format(__version__)
                        with open('Projectfile', 'w+') as f:
                            f.write(projectfile_content)
                        print('Projectfile created. Use the "p" command to invoke the manual.')
                else:
                    print('\n You are not inside any of your projects. Use the "p" command to navigate into one.')
                return
            elif args[0] in ['-h', '--help']:
                pydoc.pager(help_text)
                return
            elif args[0] in ['-w', '--walk']:
                if paths.inside_project(conf['projects-path']):
                    projectfile.get_walk_order(os.getcwd())
                else:
                    print('You are not inside any of your projects. Use the "p" command to navigate into one.')
                return
            elif args[0] in ['-p']:
                handle_project_selection(conf)

        if paths.inside_project(conf['projects-path']):
            handle_inside_project(args, conf)
        else:
            handle_project_selection(conf)

    except projectfile.error.ProjectfileError as e:
        error = e.args[0]
        message = 'Projectfile error!\n{}'.format(error['error'])
        if 'path' in error:
            message = '{}\nPath: {}/Projectfile'.format(message, error['path'])
        if 'line' in error:
            message = '{}\nLine: {}'.format(message, error['line'])
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

