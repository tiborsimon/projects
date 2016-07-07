#PROJECTS - the intuitive project manager

[![Gitter](https://img.shields.io/gitter/room/tiborsimon/projects.svg?maxAge=2592000)](https://gitter.im/tiborsimon/projects?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/tiborsimon/projects.svg?branch=master)](https://travis-ci.org/tiborsimon/projects)
[![Coveralls](https://img.shields.io/coveralls/tiborsimon/projects.svg?maxAge=2592000)](https://coveralls.io/github/tiborsimon/projects)
[![PyPI](https://img.shields.io/pypi/v/projects.svg?maxAge=2592000)](https://pypi.python.org/pypi?name=projects&version=0.1.1&:action=display)
[![license](https://img.shields.io/github/license/tiborsimon/projects.svg?maxAge=2592000)](https://github.com/tiborsimon/projects#license)
[![PyPI](https://img.shields.io/pypi/dm/projects.svg?maxAge=2592000)](https://pypi.python.org/pypi?name=projects&version=0.1.1&:action=display)
[![Status](https://img.shields.io/badge/status-under_development-yellow.svg)]()

___<projects>___ is an easy to use project navigator with a Makefile-like scripting engine. You write Projectfiles instead of Makefiles where you can document your project and you can create an interface for your users.

It works on every UNIX system with Python (2.7+ 3.x) installed. It's main purpose is to provide a simpler scripting interface with a built in documentation system. It's main target is any open source projects that want to be more user friendly from the first use. <projects> designed to minimize the typing.

__<projects>__ is not a replacement for Makefile or CMake it is an optional wrapper for them.

### Features
- quick project navigation
- Projectfile based recursive scripting system
- instant help menu generation

### Usage
```
p
p p
p <command>
p (-h|--help)
p (-v|--version)
p (-i|--init)
p (-w|--walk)
p (-l|--list) <command>
p (-md|--markdown) [<file_name>]
```

```
p
```

This command is the main trigger for projects. It behaves differently depending on your current working directory.

_OUTSIDE_ your projects directory, it opens the project selector screen, where you can select your project by typing the projects name or by using the arrows keys.

_INSIDE_ any of your projects (inside the repository root directory) this command will show the manual generated from the Projectfiles.


```
p p
```

This command behaves the same as the previous `p` command but it will always display the project selector screen. This could be handy if you want to switch projects quickly.

This is the only prohibited command name that you cannot use for your commands.


```
p <command>
```

This is the command for executing commands defined in the Projectfiles. By convention all defined command should start with an alphanumeric character. The commands started with a dash reserved for <projects> itself.

The <command> keyword can be anything except the already taken keywords:

`p`, `-h`, `--help`, `-v`, `--version`, `-i`, `--init`, `-w`, `--walk`, `-l`, `--list`


```
p (-h|--help)
```

Brings up this help screen.


```
p (-v|--version)
```

Prints out the current __<projects>__ version.


```
p (-i|--init)
```

Generates a template Projectfile into the current directory.


```
p (-w|--walk)
```

Lists out all directories in your project in the walk order __<projects>__ will follow. It marks the directories that contain a Projectfile.


```
p (-l|--list) <command>
```

Lists out the processed command bodies for the given command.


```
p (-md|--markdown) [<file_name>]
```

Generates a Markdown file from your processed Projectfiles. You can optionally specify a name for teh generated file. The default name is README.md.


# Projectfile

Projectfiles are the files you create in order to define commands that will be executed with the "p <command>". Projectfiles provide a powerful and self explanatory way to interact with your project.

You can create an example Projectfile with the `p (-i|--init)` command. The generated Projectfile will demonstrate all provided functionality except the recursive command concatenation since it will generate only one Projectfile.

There are mandatory and optional features you can add to Projectfile.

#### Mandatory

- __<projects>__ version
- at least one command definition header
- command body

#### Optional

- main description
- variables
- command alternatives
- command dependency list
- command description
- recursive separator

There is a strict order where you can place each features. Between each feature arbitrary number of empty lines are allowed. The order is the following:

1. version
1. main description
1. variables
1. command header
1. command description
1. command body (pre, separator and post)


#### version [mandatory]

```
v1.0.0
...
```

This feature will define the earliest version that is compatible with the used Projectfile format. All <projects> versions greater or equal to the defined one will be compatible with the format, but earlier versions may have problems with future features. The first release version is v1.0.0.

If there are more Projectfiles in your project and the defined versions are different, the smallest version will be used to maximize the functionality.


#### main description  [optional]

```
...
"""
Description for the whole project.
"""
...
```

After the version you can define a global description of the whole project. You can write long lines, __<projects>__ will wrap them according to the defined `doc-width` key in the __~/.prc__ configuration file. Single line breaks won't break the lines in the generated manual. You have to use an empty line in order to add a line break.

    If you have multiple Projectfiles created, the main descriptions will be
    concatenated with empty lines according to the walk order.


 #### variables  [optional]
 
```
...
variable = 42
other_variable = "This is a string with spaces"
yet_another_variable = Quotes are optional. This is still valid.
...
```

You can define variables as well. Each variable will be used as a string. No other variable format is currently supported. You can omit the quotes if you want, __<projects>__ will use the entire string you write after the `=` sign.

To use the variables you need to escape them:

```
$variable
${{variable}}
```

Both escapement is interpreted equally.

Defined variables go to the global variable pool. You cannot assign a variable the more than once. Hence you cannot redefine a variable in a later Projectfile (a Projectfile is thant is processed later according to the walk order). Redefining a variable will raise an error. Since every variables go to the global variable pool, you can use the variables in any Projectfile independently which Projectfile you defined them. It is possible to use a variable in the root level Projectfile that is defined in a later Projectfile.


#### command header  [mandatory]
```
...
my_command|alternative1|alt2: [dependency1, dependency2]
...
```

The command header feature allows you to define a command, it's alternatives and it's dependent other commands. The first keyword is the default keyword for the command. Alternatives are separated with the pipe `|` character. After the keyword definitions, a colon `:` closes the command header. After the colon, you can define a list of other commands, that are executed in the order you defined them before the current command execution.

According to the given example you can invoke your command with the following syntax inside your project directory:

`p my_command`
`p alternative1`
`p alt2`

Both will execute the same command body after the dependent commands (dependency1 and  dependency2) is executed first in the given order.

A command cannot be redefined in the same Projectfile twice. If you redefine a command in another Projectfile, the commands' bodies will be appended to each other according to the path relationship of these files.


#### command description  [optional]
```
...
my_command:
  """
  This is a command description.
  """
...
```

The command description will be added to the generated manual. It behaves the same as the main description, except it requires an indentation in any way (space, tab, count doesn't matter).

If a command is redefined in another Projectfile, the command descriptions will be appended according to the path relationship of these files.


#### command body  [mandatory]
```
...
my_command:
  command1
  command2
...  
```

The command body defines what commands __<projects>__ needs to execute if you invoke the given command with the `p <command>` syntax inside your project directory. Commands needs to be indented in any way (at least one space). __<projects>__ will execute all given commands line by line.


## Projectfile examples

Simple example

If you have multiple Projectfiles in your project and there are command headers that are defined in more than one Projectfile, the command bodies will be appended according to the path relationship of these files.

```
╔═══════════════════════════════════╦═══════════════════════════════════╗
║ $ cat ./Projectfile               ║ $ cat ./dir/Projectfile           ║
║ from v1.0.0                       ║ from v1.0.0                       ║
║ my_command:                       ║ my_command:                       ║
║   echo "This is the root."        ║   echo "This is a subdir."        ║
╠═══════════════════════════════════╩═══════════════════════════════════╣
║ $ p --walk                                                            ║
║ [x] .                                                                 ║
║ [x] dir                                                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║ $ p --list my_command                                                 ║
║ cd /home/user/projects/example                                        ║
║ echo "This is the root."                                              ║
║ cd /home/user/projects/example/dir                                    ║
║ echo "This is the a subdir."                                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║ $ p my_command                                                        ║
║ This is the root.                                                     ║
║ This is a subdir.                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

#### What you can notice in this example

- You can use the `(-w|--walk)` and `(-l|--list)` commands to get information about the commands will be executed by __<projects>__.
- The command listing shows that the command bodies were concatenated according to the walk order (you can check with the `(-w|--walk)` command).
- The concatenated command list contains directory change commands (cd) so every command defined in a Projectfile gets executed in the same directory level as it's Projectfile's directory level.
- Thus the directory change commands, you can notice that each command will execute in the same execution context regardless of the command's length (number of lines). This is different than the Makefile conventions, and provide a much more simpler script writing.


### More complex example

There is another feature that can be used to execute post configuration eg. executing commands after all lower order command bodies were executed. This feature is called recursive separator (`===`). If you place this separator inside a command's body, and there are other lower level Projectfiles in your project, the command bodies will be appended in a special, recursive order.

In a Projectfile, all commands before the separator are called the __pre__ commands, and all the commands after the separator are called the __post__ commands. The seprator in every command body is optional. If there is no separator, all the command lines in the command body will be handled as a __pre__ command block. Similarly if the command body starts with a separator the whole body will be used as a post block.

If there are no lower level Projectfiles, and you have a command with separated body, the sepration will be ignored.

If you have lower level Projectfiles, the base level pre commands will be executed first then the execution will jump to the lower level Projectfile. After the lower level Projectfile's command script gets executed, the execution will be jump back after the base level separator, and the base post block will be executed.

If the lower level Projectfile has separated command bodies, and there are yet another lower level Projectfile, the execution will jump down recursively until the last possible separation is executed.

The following example will demonstrate this behavior:

```
╔═══════════════════════════════════╦═══════════════════════════════════╗
║ $ cat ./Projectfile               ║ $ cat ./A/Projectfile             ║
║ from v1.0.0                       ║ from v1.0.0                       ║
║ my_command:                       ║ my_command:                       ║
║   echo "pre root"                 ║   echo "pre A"                    ║
║   ===                             ║   ===                             ║
║   echo "post root"                ║   echo "post A"                   ║
╠═══════════════════════════════════╬═══════════════════════════════════╣
║ $ cat ./A/B/Projectfile           ║ $ cat ./C/Projectfile             ║
║ from v1.0.0                       ║ from v1.0.0                       ║
║ my_command:                       ║ my_command:                       ║
║   echo "listing inside A/B"       ║   echo "pre C"                    ║
║   ls -1                           ║   ===                             ║
║   echo "done"                     ║   echo "post C"                   ║
╠═══════════════════════════════════╩═══════════════════════════════════╣
║ $ ls -1 A/B                                                           ║
║ Projectfile                                                           ║
║ file1                                                                 ║
║ file2                                                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║ $ p --walk                                                            ║
║ [x] .                                                                 ║
║ [x] A                                                                 ║
║ [x] A/B                                                               ║
║ [x] C                                                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║ $ p --list my_command                                                 ║
║ cd /home/user/projects/example                                        ║
║ echo "pre root"                                                       ║
║ cd /home/user/projects/example/A                                      ║
║ echo "pre A"                                                          ║
║ cd /home/user/projects/example/A/B                                    ║
║ echo "listing inside A/B"                                             ║
║ ls -1                                                                 ║
║ echo "done"                                                           ║
║ cd /home/user/projects/example/A                                      ║
║ echo "post A"                                                         ║
║ cd /home/user/projects/example/C                                      ║
║ echo "pre C"                                                          ║
║ echo "post C"                                                         ║
║ cd /home/user/projects/example                                        ║
║ echo "post root"                                                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║ $ p my_command                                                        ║
║ pre root                                                              ║
║ pre A                                                                 ║
║ listing inside A/B                                                    ║
║ Projectfile                                                           ║
║ file1                                                                 ║
║ file2                                                                 ║
║ done                                                                  ║
║ post A                                                                ║
║ pre C                                                                 ║
║ post C                                                                ║
║ post root                                                             ║
╚═══════════════════════════════════════════════════════════════════════╝
```

#### What you can notice in this example

- The recursive separators works as described. The post commands are executed after the pre commands for that level and all the recursive lower level other commands executed.
- Commands get executed in the same level where the Projectfile they are defined in is located.
- Automatic directory changing command insertion is smart enough to insert only the absolute necessary directory changing commands. If there are no lower level commands, but the recursive separator exists, no directory changing will be inserted before the post commands. If there are no pre commands, no directory cahnging will be happen before the recursive separator content. Same goes to the post commands. If there are no post commands, no directory changing commands will be inserted after the recursive separator's content is executed.

TIP: You can always create a template Projectfile with the `(-i|--init)` command.


## License

This project is under the __MIT license__. 
See the included license file for further details.

```
Copyright (c) 2016 Tibor Simon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
