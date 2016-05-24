#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import error
from . import parser
from . import file_handler


def generate_processing_tree(project_root):
    """Generates the preprocessed Projectfile data tree. The generated data structure maps the
    Projectfile-containing directories hierarchy. The data generation will be started from the given
    project root path. The function iteratively will parse the existing Projectfiles one by one based
    on the given pluggable walk-like path generator.

    Output data format:

    processing_tree = [
        {
            'path': 'path for the first folder containing a Projectfile',
            'min-version': (1, 2, 3),
            'description': 'Optional general description.',
            'variables': {
                'variable_1: {
                    'value': '42',
                    'path': 'path for the first folder containing a Projectfile'
                },
                ...
            }
            'commands': {
                'command_1': {
                    'description': 'Command level description for command_1.',
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
    data = []
    stack = []

    walk_data = file_handler.projectfile_walk(project_root)

    # TODO: implement pluggable walk_data creation

    for path, lines in walk_data:
        node = _create_node(path, lines)
        _pop_stack_until_common_node(stack, path)
        if stack:
            _chain_data_to_last_element(stack, node)
        else:
            stack = _initialize_stack(data, node)
    return data


def _create_node(path, raw_lines):
    node = {
        'path': path,
        'children': []
    }
    try:
        node.update(parser.process_lines(raw_lines))
    except error.ProjectfileError as e:
        try:
            msg = e.message
        except AttributeError:
            msg = e.msg
        msg.update({'path': path})
        raise error.ProjectfileError(msg)
    return node


def _pop_stack_until_common_node(stack, path):
    while stack and not path.startswith(stack[-1]['path']):
        stack.pop()


def _chain_data_to_last_element(stack, node):
    stack[-1]['children'].append(node)
    stack.append(node)


def _initialize_stack(data, node):
    data.append(node)
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
    data = {'commands': {}}
    command_buffer = data['commands']

    for node in input_data:
        _process_node(command_buffer, node, data)
    return data


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


def _add_version(node, data):
    if 'min-version' in data:
        if data['min-version'] < node['min-version']:
            data['min-version'] = node['min-version']
    else:
        data['min-version'] = node['min-version']


def _add_main_description(node, data):
    if 'description' in node:
        if 'description' in data:
            data['description'] += '\n\n' + node['description']
        else:
            data['description'] = node['description']


def _command_names(node):
    return list(node['commands'].keys())


def _delete_divisors(commands):
    for name in commands:
        command = commands[name]
        command['script'] = [l for l in command['script'] if l != '===']


def _process_children(command_buffer, node, data):
    if node['children']:
        for child in node['children']:
            _process_node(command_buffer, child, data)
    else:
        _delete_divisors(command_buffer)


def create_working_pool(command_buffer, command_name):
    if command_name not in command_buffer:
        command_buffer[command_name] = {'script': []}
    pool = command_buffer[command_name]
    return pool


def _process_commands(command_buffer, node):
    for command_name in _command_names(node):
        pool = create_working_pool(command_buffer, command_name)
        raw_command = node['commands'][command_name]

        _add_command_description(pool, raw_command)
        _add_cd(pool, node)
        _add_pre(pool, raw_command)
        _add_divisor(pool)
        _add_post(pool, raw_command)


def _add_variables(node, data):
    if 'variables' in node:
        if 'variables' not in data:
            data['variables'] = {}
        for name in node['variables']:
            if name in data['variables']:
                raise error.ProjectfileError({
                    'error': error.VARIABLE_REDEFINED_ERROR.format(name, data['variables'][name]['path'], node['path']),
                    'path': node['path']
                })
            else:
                data['variables'][name] = {
                    'value': node['variables'][name],
                    'path': node['path']
                }


def _process_node(command_buffer, node, data):
    _process_commands(command_buffer, node)
    _process_children(command_buffer, node, data)
    _add_version(node, data)
    _add_main_description(node, data)
    _add_variables(node, data)


def process_variables(data):
    """This function will replace all variables in all commands and descriptions. After the replacement
    it will delete the 'variables' part of the data.

    :param data: Finalized data structure. the processing will be applied in place.
    :return: None
    """
    if 'variables' in data:
        for command_name in data['commands']:
            command = data['commands'][command_name]
            _apply_variables_to_command_description(command, data)
            _apply_variables_to_command_lines(command, data)
        _apply_variables_to_main_description(data)
        del data['variables']


def _apply_variables_to_command_description(command, data):
    if 'description' in command:
        for var_name in data['variables']:
            command['description'] = command['description'].replace(var_name, data['variables'][var_name]['value'])


def _apply_variables_to_command_lines(command, data):
    temp_lines = []
    for line in command['script']:
        line = line
        for var_name in data['variables']:
            line = line.replace(var_name, data['variables'][var_name]['value'])
        temp_lines.append(line)
    command['script'] = temp_lines


def _apply_variables_to_main_description(data):
    if 'description' in data:
        for var_name in data['variables']:
            data['description'] = data['description'].replace(var_name, data['variables'][var_name]['value'])
