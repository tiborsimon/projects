#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import error
from . import parser
from . import file_handler


def data_integrity_check(data):
    """Checks if all command dependencies refers to and existing command. If not, a ProjectfileError
    will be raised with the problematic dependency and it's command.

    :param data: parsed raw data set.
    :return: None
    """
    deps = []
    for command in data['commands']:
        if 'dependencies' in data['commands'][command]:
            for d in data['commands'][command]['dependencies']:
                deps.append({
                    'd': d,
                    'c': command
                })
    for d in deps:
        if d['d'] not in data['commands']:
            raise error.ProjectfileError({
                'error': error.PROJECTFILE_INVALID_DEPENDENCY.format(d['d'], d['c'])
            })


def generate_processing_tree(project_root):
    """Generates the preprocessed Projectfile data tree. The generated data structure maps the
    Projectfile containing directory nodes. The data generation will be started from the given
    project root path. The function iteratively will parse the existing Projectfiles in the
    directory structure based on the given pluggable walk-like path generator.

    Output data format:

    processing_tree = [
        {
            'path': 'path for the first folder containing a Projectfile',
            'min-version': (1, 2, 3),
            'description': 'General description.',
            'commands': {
                'command_1': {
                    'description': 'Command level description for command_1.',
                    'pre': ['pre', 'command', 'list', ... ],
                    'post': ['post', 'command', 'list', ... ]
                },
                'command_2': {
                    'description': 'Command level description for command_2.',
                    'pre': ['pre', 'command', 'list', ... ],
                    'post': ['post', 'command', 'list', ... ]
                },
                ...
            },
            children: [
                {
                    # same dictionary as the outer one
                },
                {
                    # same dictionary as the outer one
                },
                ...
            ]
        }
    ]

    :param project_root: root of the project.
    :return: generated processing tree
    """
    ret = []
    stack = []

    for path, lines in file_handler.projectfile_walk(project_root):
        node = _create_node(path, lines)
        _pop_stack_until_common_node(stack, path)
        if stack:
            _chain_data_to_last_element(stack, node)
        else:
            stack = _initialize_stack(ret, node)
    return ret


def _create_node(path, raw_lines):
    temp = {
        'path': path,
        'children': []
    }
    temp.update(parser.process_lines(raw_lines))
    return temp


def _pop_stack_until_common_node(stack, path):
    while stack and not path.startswith(stack[-1]['path']):
        stack.pop()


def _chain_data_to_last_element(stack, node):
    stack[-1]['children'].append(node)
    stack.append(node)


def _initialize_stack(ret, node):
    ret.append(node)
    return [node]


def finalize_data(input_data):
    """Flattens out passed preprocessed data tree and generates the final usage ready
    data structure. The function will select the latest version specified in the
    Projectfiles as the minimum required software version. If there are multiple
    Projectfiles specifying the same description, the individual descriptions will be
    appended together with a line break.

    Output data format:

    data = {
        'min-version': (1, 2, 3),
        'description': 'General description.',
        'commands': {
            'command_1': {
                'description': 'Command level description for command_1.',
                'script': [
                    'flattened',
                    'out command',
                    'list for',
                    'command_1',
                    ...
                ]
            },
            'command_2': {
                'description': 'Command level description for command_2.',
                'script': [
                    'flattened',
                    'out command',
                    'list for',
                    'command_2',
                    ...
                ]
            },
            ...
        }
    }

    :param input_data: preprocessed data tree
    :return: final data structure
    """
    ret = {'commands': {}}
    command_buffer = ret['commands']

    for node in input_data:
        _process_node(command_buffer, node, ret)
    return ret


def _add_cd(pool, node):
    try:
        index = pool['script'].index('===')
        pool['script'].remove('===')
        pool['script'].insert(index, 'cd ' + node['path'])
        index += 1
        pool['script'].insert(index, '===')
    except ValueError:
        pool['script'].append('cd ' + node['path'])


def _add_pre(pool, raw_command):
    try:
        index = pool['script'].index('===')
        pool['script'].remove('===')
        for line in raw_command['pre']:
            pool['script'].insert(index, line)
            index += 1
        pool['script'].insert(index, '===')
    except ValueError:
        pool['script'].extend(raw_command['pre'])


def _add_divisor(pool):
    if '===' not in pool['script']:
        pool['script'].append('===')


def _add_post(pool, raw_command):
    if 'post' in raw_command:
        try:
            index = pool['script'].index('===')
            index += 1
            for line in raw_command['post']:
                pool['script'].insert(index, line)
                index += 1
        except ValueError:
            pool['script'].extend(raw_command['post'])


def _add_command_description(pool, raw_command):
    if 'description' in raw_command:
        if 'description' in pool:
            pool['description'] += '\n\n' + raw_command['description']
        else:
            pool['description'] = raw_command['description']


def _add_version(node, ret):
    if 'min-version' in ret:
        if ret['min-version'] < node['min-version']:
            ret['min-version'] = node['min-version']
    else:
        ret['min-version'] = node['min-version']


def _add_main_description(node, ret):
    if 'description' in node:
        if 'description' in ret:
            ret['description'] += '\n\n' + node['description']
        else:
            ret['description'] = node['description']


def _command_names(node):
    return list(node['commands'].keys())


def _delete_divisors(commands):
    for name in commands:
        command = commands[name]
        command['script'] = filter(lambda l: l != '===', command['script'])


def _process_children(command_buffer, node, ret):
    if node['children']:
        for child in node['children']:
            _process_node(command_buffer, child, ret)
    else:
        _delete_divisors(command_buffer)


def _process_commands(command_buffer, node):
    for command_name in _command_names(node):
        if command_name not in command_buffer:
            command_buffer[command_name] = {'script': []}

        pool = command_buffer[command_name]
        raw_command = node['commands'][command_name]

        _add_command_description(pool, raw_command)
        _add_cd(pool, node)
        _add_pre(pool, raw_command)
        _add_divisor(pool)
        _add_post(pool, raw_command)


def _process_node(command_buffer, node, ret):
    _process_commands(command_buffer, node)
    _process_children(command_buffer, node, ret)
    _add_version(node, ret)
    _add_main_description(node, ret)
