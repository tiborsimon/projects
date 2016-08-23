#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pydoc
import subprocess
import sys
import signal

from pkg_resources import get_distribution
from termcolor import colored

from projects import config
from projects import gui
from projects import paths
from projects import projectfile

__version__ = get_distribution('projects').version

help_text = '''\
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

<projects> is  an  easy to  use project  navigation  tool  and  a Makefile-like
scripting engine. It's main purpose is to provide a simpler scripting interface
with a built in man page generator.  You can  define  your commands with inline
documentation in Projectfiles.  You can have one Projectfile in every directory
inside your project, <projects> will process them recursively.

<projects> works on every UNIX system with Python 2.7+ or 3.x installed.

<projects> is not a replacement for Makefile or CMake it is an optional wrapper
for them.

Features:
  - quick project navigation with minimal typing
  - Projectfile based recursive scripting system
  - command concatenation and recursive separation
  - automatic manual page generation


Configuration

  When  projects  starts  up for the first time, it creates it's  configuration
  file (only if it isn't exist already) inside your home directory: ~/.prc

  By default it contains the following options in YAML format:

  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ $ cat ~/.prc                                                              ║
  ║ max-doc-width: 80                                                         ║
  ║ projects-path: ~/projects                                                 ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  projects-path  [mandatory]

    It's value will tell projects where it can find your projects' repositories

  max-doc-width  [optional]

    The maximum width of the generated manual pages. If not defined, it will be
    set to 80. <projects> will adapt to narrower terminals.


Usage:
  p
  p p
  p <command>
  p (-h|--help)
  p (-v|--version)
  p (-i|--init)
  p (-w|--walk)
  p (-l|--list) <command>
  p (-md|--markdown) [<file_name>]


p

  This command  is  the main  trigger  for  projects.  It  behaves  differently
  depending on your current working directory.

  OUTSIDE your projects directory,  it opens the project selector screen, where
  you can select your  project  by  typing  the projects name  or  by using the
  arrows keys.

  INSIDE  any  of  your  projects  (inside the repository root directory)  this
  command will show the manual generated from the Projectfiles.


p p

  This command behaves the same  as the previous "p" command but it will always
  display  the  project  selector  screen.  This could be handy  if you want to
  switch projects quickly.

  This  is  the  only  prohibited  command  name  that  you cannot use for your
  commands.


p <command>

  This is the command  for  executing commands defined in the Projectfiles.  By
  convention  all  defined command should start with an alphanumeric character.
  The commands started with a dash reserved for <projects> itself.

  The <command> keyword can be anything except the already taken keywords:
  p, -h, --help, -v, --version, -i, --init, -w, --walk, -l, --list


p (-h|--help)

  Brings up this help screen.


p (-v|--version)

  Prints out the current <projects> version.


p (-i|--init)

  Generates a template Projectfile into the current directory.


p (-w|--walk)

  Lists out all directories in your project in the walk order  <projects>  will
  follow. It marks the directories that contain a Projectfile.


p (-l|--list) <command>

  Lists out the processed command bodies for the given command.


p (-md|--markdown) [<file_name>]

  Generates  a  Markdown  file  from  your  processed  Projectfiles.   You  can
  optionally  specify  a  name  for  the  generated  file.  The default name is
  README.md.




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

Projectfiles are the files you  create in order to define commands that will be
executed  with  the  "p <command>".  Projectfiles  provide  a powerful and self
explanatory way to interact with your project.

You  can  create  an example Projectfile with the "p (-i|--init)" command.  The
generated  Projectfile  will  demonstrate all provided functionality except the
recursive command concatenation since it will generate only one Projectfile.

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

Feature order:
  There  is  a  strict  order  where you can place each features.  Between each
  feature  arbitrary  number  of  empty  lines  are  allowed.  The order is the
  following:

  1. version
  2. main description
  3. variables
  4. command header
  5. command description
  6. command body (pre, separator and post)


version [mandatory]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ from v{version}                                                               ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  This  feature  will  define  the earliest version that is compatible with the
  used Projectfile format.  All  <projects>  versions greater  or  equal to the
  defined one will be compatible with the format, but earlier versions may have
  problems with future features. The first release version is v1.0.0.

  If there are more Projectfiles in  your project  and the defined versions are
  different, the smallest version will be used to maximize the functionality.


main description  [optional]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ...                                                                       ║
  ║ """                                                                       ║
  ║ Description for the whole project.                                        ║
  ║ """                                                                       ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  After  the  version you can define a global description of the whole project.
  You can write long lines, <projects> will wrap them according to the defined
  "max-doc-width" key in the ~/.prc configuration  file.  Single  line  breaks
  won't break the lines in the generated manual. You have to use an empty line
  in order to add a line break.

  If  you  have  multiple  Projectfiles created, the main descriptions will be
  concatenated with empty lines according to the walk order.


variables  [optional]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ...                                                                       ║
  ║ variable = 42                                                             ║
  ║ other_variable = "This is a string with spaces"                           ║
  ║ yet_another_variable = Quotes are optional. This is still valid.          ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  You can define variables as well. Each variable will be used as a string.  No
  other variable format is currently supported.  You can omit the quotes if you
  want, <projects> will use the entire string you write after the "=" sign.

  To use the variables you need to escape them:

    $variable
    ${{variable}}

  Both escapement is interpreted equally.

  Defined  variables  go  to  the  global  variable  pool.  You cannot assign a
  variable the more than once.  Hence you cannot redefine a variable in a later
  Projectfile (a Projectfile is thant is processed later  according to the walk
  order).  Redefining a variable will raise an error.  Since every variables go
  to  the  global  variable pool,  you can use the variables in any Projectfile
  independently  which  Projectfile  you defined them.  It is possible to use a
  variable  in  the  root  level   Projectfile  that  is  defined  in  a  later
  Projectfile.


command header  [mandatory]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ...                                                                       ║
  ║ my_command|alternative1|alt2: [dependency1, dependency2]                  ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  The command header feature allows you to define a command,  it's alternatives
  and it's dependent other commands.  The first keyword is  the default keyword
  for the command.  Alternatives  are  separated  with the  pipe "|" character.
  After the keyword definitions,  a colon ":" closes the command header.  After
  the colon,  you can define a list of other commands, that are executed in the
  order you defined them before the current command execution.

  According to the given example you can invoke your command with the following
  syntax inside your project directory:

    p my_command
    p alternative1
    p alt2

  Both  will  execute  the  same  command  body  after  the  dependent commands
  (dependency1 and dependency2) is executed first in the given order.

  A command cannot be redefined in the same Projectfile twice.  If you redefine
  a command in another Projectfile,  the commands' bodies will be  appended  to
  each other according to the path relationship of these files.


command description  [optional]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ...                                                                       ║
  ║ my_command:                                                               ║
  ║   """                                                                     ║
  ║   This is a command description.                                          ║
  ║   """                                                                     ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  The command description will be added to the generated manual. It behaves the
  same as the main description,  except  it  requires an indentation in any way
  (space, tab, count doesn't matter).

  If  a  command is redefined in another Projectfile,  the command descriptions
  will be appended according to the path relationship of these files.


command body  [mandatory]
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ...                                                                       ║
  ║ my_command:                                                               ║
  ║   command1                                                                ║
  ║   command2                                                                ║
  ║ ...                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  The  command  body  defines  what commands <projects> needs to execute if you
  invoke the given command with the  "p <command>"  syntax  inside your project
  directory.  Commands needs  to be indented  in any way  (at least one space).
  <projects> will execute all given commands line by line.


Template Projectfile

  The following Projectfile can be generated with the `p (-i|--init)` command:

  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ from v1.0.0                                                               ║
  ║                                                                           ║
  ║ """                                                                       ║
  ║ This is a template Projectfile you have created with the 'p (-i|--init])' ║
  ║ command. You can use the provided commands 'hello' and 'answer' or it's   ║
  ║ shorter alternatives 'h' and 'ans' or 'a'. ie.: p <command>.              ║
  ║                                                                           ║
  ║ You can start a new paragraph in the descriptions by inserting an empty   ║
  ║ line like this.                                                           ║
  ║                                                                           ║
  ║ Descriptions are useful as they provide a searchable automatically        ║
  ║ generated manual for your project for free. You can invoke this manual    ║
  ║ with the "p" command if you are inside your project directory.            ║
  ║ """                                                                       ║
  ║                                                                           ║
  ║ magic = 42  # variables goes to the global variable space                 ║
  ║                                                                           ║
  ║ hello|h: [a]                                                              ║
  ║     """                                                                   ║
  ║     This command will great you.                                          ║
  ║                                                                           ║
  ║     There is a shorter alternative "h" for the command. It is depending   ║
  ║     on the "a" command which is the alternative of the "answer" command.  ║
  ║                                                                           ║
  ║     If you execute a command with dependencies, it's dependencies will be ║
  ║     executed first in the defined order.                                  ║
  ║     """                                                                   ║
  ║     echo "Hi! This is my very own Projectfile."                           ║
  ║                                                                           ║
  ║ answer|ans|a:                                                             ║
  ║     """                                                                   ║
  ║     This command will give you the answer for every question.             ║
  ║                                                                           ║
  ║     You can use the long "answer" keyword as well as the shorter "ans" or ║
  ║     "a" to execute this command.                                          ║
  ║                                                                           ║
  ║     Inside the Projectfile, you can also refer to a command in another    ║
  ║     command's dependency list by any of it's alternatives.                ║
  ║     """                                                                   ║
  ║     echo "The answer for everything is $magic!"                           ║
  ║     # you can also use the ${{magic}} form                                  ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  If you use the "p" command inside your project's root directory,projects will
  generate  a manual page  from the Projectfiles  you  created.  The previously
  listed Projectfile will result  the  following manual page assuming that your
  project is called "example"  (the project name is picked from it's containing
  directory's name):

  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║ ========================================================================= ║
  ║                              E X A M P L E                                ║
  ║ ========================================================================= ║
  ║                                                                           ║
  ║ This is a template Projectfile you have created with the "p (-i|--init])" ║
  ║ command. You can use the provided commands 'hello' and 'answer' or it's   ║
  ║ shorter alternatives 'h' and 'ans' or 'a'. ie.: p <command>.              ║
  ║                                                                           ║
  ║ You can start a new paragraph in the descriptions by inserting an empty   ║
  ║ line like this.                                                           ║
  ║                                                                           ║
  ║ Descriptions are useful as they provide a searchable automatically        ║
  ║ generated manual for your project for free. You can invoke this manual    ║
  ║ with the "p" command if you are inside your project directory.            ║
  ║                                                                           ║
  ║                                                                           ║
  ║ answer|ans|a:                                                             ║
  ║                                                                           ║
  ║     This command will give you the answer for every question.             ║
  ║                                                                           ║
  ║     You can use the long "answer" keyword as well as the shorter "ans" or ║
  ║     "a" to execute this command.                                          ║
  ║                                                                           ║
  ║     Inside the Projectfile, you can also refer to a command in another    ║
  ║     command's dependency list by any of it's alternatives.                ║
  ║                                                                           ║
  ║                                                                           ║
  ║ hello|h: [a]                                                              ║
  ║                                                                           ║
  ║     This command will great you.                                          ║
  ║                                                                           ║
  ║     There is a shorter alternative "h" for the command. It is depending   ║
  ║     on the "a" command which is the alternative of the "answer" command.  ║
  ║                                                                           ║
  ║     If you execute a command with dependencies, it's dependencies will be ║
  ║     executed first in the defined order.                                  ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  This manual is displayed in a pager, so you can exit with the "q" key.


Advanced Projectfile examples

  Command concatenation

  If  you  have  multiple  Projectfiles  in  your project and there are command
  headers  that  are  defined  in more than one Projectfile, the command bodies
  will be appended according to the path relationship of these files.

  ╔═════════════════════════════════════╦═════════════════════════════════════╗
  ║ $ cat ./Projectfile                 ║ $ cat ./dir/Projectfile             ║
  ║ from v{version}                         ║ from v{version}                         ║
  ║ my_command:                         ║ my_command:                         ║
  ║   echo "This is the root."          ║   echo "This is a subdir."          ║
  ╠═════════════════════════════════════╩═════════════════════════════════════╣
  ║ $ p --walk                                                                ║
  ║ [x] .                                                                     ║
  ║ [x] dir                                                                   ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║ $ p --list my_command                                                     ║
  ║ cd /home/user/projects/example                                            ║
  ║ echo "This is the root."                                                  ║
  ║ cd /home/user/projects/example/dir                                        ║
  ║ echo "This is the a subdir."                                              ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║ $ p my_command                                                            ║
  ║ This is the root.                                                         ║
  ║ This is a subdir.                                                         ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  What you can notice in this example:
    1. You  can  use  the  "(-w|--walk)"  and  "(-l|--list)"  commands  to  get
       information about the commands will be executed by <projects>.
    2. The  command  listing  shows  that  the command bodies were concatenated
       according  to  the  walk  order  (you  can check with the  "(-w|--walk)"
       command).
    3. The  concatenated  command  list contains directory change commands (cd)
       so  every  command  defined  in  a Projectfile gets executed in the same
       directory level as it's Projectfile's directory level.
    4. Thus  the  directory  change commands,  you can notice that each command
       will  execute  in the same execution context regardless of the command's
       length  (number  of  lines).    This  is  different  than  the  Makefile
       conventions, and provide a much more simpler script writing.


  More complex example

  There  is  another feature that can be used to execute post configuration eg.
  executing commands after  all lower order command bodies were executed.  This
  feature is  called  recursive separator ("===").  If you place this separator
  inside a command's body, and there are other lower level Projectfiles in your
  project, the command bodies will be appended in a special, recursive order.

  In  a  Projectfile ,  all  commands before the separator are called the "pre"
  commands,  and all  the  commands  after  the separator are called the "post"
  commands.  The seprator in every  command body  is  optional.  If there is no
  separator,  all  the  command  lines in the command body will be handled as a
  "pre" command block.  Similarly  if  the command body starts with a separator
  the whole body will be used as a post block.

  If  there  are no lower level Projectfiles,  and  you  have  a  command  with
  separated body, the sepration will be ignored.

  If  you  have  lower  level Projectfiles, the base level pre commands will be
  executed first  then  the execution will jump to the lower level Projectfile.
  After  the  lower  level  Projectfile's  command  script  gets  executed, the
  execution will be jump back after the base level separator, and the base post
  block will be executed.

  If  the lower level Projectfile has separated  command bodies,  and there are
  yet  another  lower  level   Projectfile,    the  execution  will  jump  down
  recursively until the last possible separation is executed.

  The following example will demonstrate this behavior:

  ╔═════════════════════════════════════╦═════════════════════════════════════╗
  ║ $ cat ./Projectfile                 ║ $ cat ./A/Projectfile               ║
  ║ from v{version}                         ║ from v{version}                         ║
  ║ my_command:                         ║ my_command:                         ║
  ║   echo "pre root"                   ║   echo "pre A"                      ║
  ║   ===                               ║   ===                               ║
  ║   echo "post root"                  ║   echo "post A"                     ║
  ╠═════════════════════════════════════╬═════════════════════════════════════╣
  ║ $ cat ./A/B/Projectfile             ║ $ cat ./C/Projectfile               ║
  ║ from v{version}                         ║ from v{version}                         ║
  ║ my_command:                         ║ my_command:                         ║
  ║   echo "listing inside A/B"         ║   echo "pre C"                      ║
  ║   ls -1                             ║   ===                               ║
  ║   echo "done"                       ║   echo "post C"                     ║
  ╠═════════════════════════════════════╩═════════════════════════════════════╣
  ║ $ ls -1 A/B                                                               ║
  ║ Projectfile                                                               ║
  ║ file1                                                                     ║
  ║ file2                                                                     ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║ $ p --walk                                                                ║
  ║ [x] .                                                                     ║
  ║ [x] A                                                                     ║
  ║ [x] A/B                                                                   ║
  ║ [x] C                                                                     ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║ $ p --list my_command                                                     ║
  ║ cd /home/user/projects/example                                            ║
  ║ echo "pre root"                                                           ║
  ║ cd /home/user/projects/example/A                                          ║
  ║ echo "pre A"                                                              ║
  ║ cd /home/user/projects/example/A/B                                        ║
  ║ echo "listing inside A/B"                                                 ║
  ║ ls -1                                                                     ║
  ║ echo "done"                                                               ║
  ║ cd /home/user/projects/example/A                                          ║
  ║ echo "post A"                                                             ║
  ║ cd /home/user/projects/example/C                                          ║
  ║ echo "pre C"                                                              ║
  ║ echo "post C"                                                             ║
  ║ cd /home/user/projects/example                                            ║
  ║ echo "post root"                                                          ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║ $ p my_command                                                            ║
  ║ pre root                                                                  ║
  ║ pre A                                                                     ║
  ║ listing inside A/B                                                        ║
  ║ Projectfile                                                               ║
  ║ file1                                                                     ║
  ║ file2                                                                     ║
  ║ done                                                                      ║
  ║ post A                                                                    ║
  ║ pre C                                                                     ║
  ║ post C                                                                    ║
  ║ post root                                                                 ║
  ╚═══════════════════════════════════════════════════════════════════════════╝

  What you can notice in this example:
    1. The  recursive  separators  works  as  described.  The post commands are
       executed after the pre commands  for  that  level  and all the recursive
       lower level other commands executed.
    2. Commands get executed in  the same  level where the Projectfile they are
       defined in is located.
    3. Automatic directory changing command insertion is smart enough to insert
       only the absolute necessary directory changing commands. If there are no
       lower level commands,  but the recursive separator exists,  no directory
       changing will be inserted before the post commands.  If there are no pre
       commands,  no  directory  cahnging  will  be happen before the recursive
       separator content. Same goes to the post commands.  If there are no post
       commands,  no  directory  changing  commands  will be inserted after the
       recursive separator's content is executed.

  TIP: You can always create a template Projectfile with the "(-i|--init)"
       command.
'''.format(version=__version__)

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
    echoed_commands = []
    for line in command['script']:
        if '&&' in line:
            line = line.split('&&')
            line = [l.strip() for l in line]
        else:
            line = [line.strip()]
        for l in line:
            if l.startswith('echo'):
                echoed_commands.append('printf "\033[1;32m> " && {0} && printf "\033[0m"'.format(l))
            elif l.startswith('cd'):
                p = l.split('cd')
                p = p[1].strip()
                echoed_commands.append('printf "\033[0;34m@ {0}\033[0m\n" && {1}'.format(p, l))
            else:
                echoed_commands.append('printf "\033[1;33m$ {0}\033[0m\n" && {0}'.format(l))
    concatenated_commands = ' && '.join(echoed_commands)
    execute_call(concatenated_commands)

def execute_call(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output, error = process.communicate()
    exit_code = process.returncode

    if exit_code != 0:
        sys.stderr.write('\r\033[1;31m[ERROR {}]\033[0;31m Error during execution!\033[0m\n'.format(exit_code))


def execute(args, data, conf):
    if args:
        for command_name in args:
            if command_name in data['commands']:
                try:
                    process_command(command_name, data)
                except (KeyboardInterrupt):
                    sigterm_handle(None, None)
            else:
                pass
    else:
        gui.show_project_details(data, conf['max-doc-width'])


def sigterm_handle(signal, frame):
    sys.stderr.write('\r\r\033[1;31m[!]\033[0;31m User interrupt..\033[0m\n')
    sys.exit(1)


def main(args):
    signal.signal(signal.SIGTSTP, sigterm_handle)
    try:
        conf = config.get()

        if not os.path.isdir(conf['projects-path']):
            os.mkdir(conf['projects-path'])
            print("Projects root was created: {}".format(conf['projects-path']))
            print("You can put your projects here.")
            with open(os.path.join(os.path.expanduser('~'), '.p-path'), 'w+') as f:
                f.write(conf['projects-path'])
            return
        else:
            if not os.listdir(conf['projects-path']):
                print("Your projects directory is empty. Nothing to do..")
                with open(os.path.join(os.path.expanduser('~'), '.p-path'), 'w+') as f:
                    f.write(conf['projects-path'])
                return

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
                    print('You are not inside any of your projects. Use the "p" command to navigate into one.')
                return

            elif args[0] in ['-h', '--help']:
                pydoc.pager(help_text)
                return

            elif args[0] in ['-w', '--walk']:
                if paths.inside_project(conf['projects-path']):
                    print(projectfile.get_walk_order(os.getcwd()))
                else:
                    print('You are not inside any of your projects. Use the "p" command to navigate into one.')
                return

            elif args[0] in ['p']:
                handle_project_selection(conf)
                return

            elif args[0] in ['-l', '--list']:
                print('Command name missing after this option. Cannot list the command body..\np (-l|--list) <command>')
                return

            elif args[0] in ['-md', '--markdown']:
                project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
                data = projectfile.get_data_for_root(project_root['path'])
                data['name'] = project_root['name']
                md_content = gui.generate_markdown(data)
                with open(os.path.join(project_root['path'], 'README.md'), 'w+') as f:
                    f.write(md_content)
                print("README.md file was generated into your project's root.")
                return

        if len(args) == 2:
            if args[0] in ['-l', '--list']:
                command = args[1]
                project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
                data = projectfile.get_data_for_root(project_root['path'])
                if command in data['commands']:
                    if 'alias' in data['commands'][command]:
                        command = data['commands'][command]['alias']
                    for line in data['commands'][command]['script']:
                        print(line)
                else:
                    print('Invalid command: "{}"\nAvailable commands:'.format(command))
                    for c in data['commands']:
                        print(c)
                return
            elif args[0] in ['-md', '--markdown']:
                name = args[1]
                project_root = paths.get_project_root(conf['projects-path'], os.getcwd())
                data = projectfile.get_data_for_root(project_root['path'])
                data['name'] = project_root['name']
                md_content = gui.generate_markdown(data)
                with open(os.path.join(project_root['path'], name), 'w+') as f:
                    f.write(md_content)
                print("A markdown file named \"{}\" was generated into your project's root.".format(name))
                return

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
        message = 'Config error!\n{}'.format(error)
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

