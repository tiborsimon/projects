#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from . import error
from . import parser
from . import file_handler


def data_integrity_check(data):
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
    """Generates the preprocessed projectfile data tree.
    :param project_root: root of the project.
    :return:
    """

    def create_node(_path, _raw_lines):
        temp = {
            'path': _path,
            'children': []
        }
        temp.update(parser.process_lines(_raw_lines))
        return temp

    def pop_stack_until_common_node(_stack, _path):
        while _stack and not _path.startswith(_stack[-1]['path']):
            _stack.pop()

    def chain_data_to_last_element(_stack, _node):
        _stack[-1]['children'].append(_node)
        _stack.append(_node)

    def initialize_stack(_ret, _node):
        _ret.append(_node)
        return [_node]

    ret = []
    stack = []

    for path, lines in file_handler.projectfile_walk(project_root):
        node = create_node(path, lines)
        pop_stack_until_common_node(stack, path)
        if stack:
            chain_data_to_last_element(stack, node)
        else:
            stack = initialize_stack(ret, node)
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
        pool['description'] = raw_command['description']


def _add_version(node, ret):
    ret['min-version'] = node['min-version']


def _add_main_description(node, ret):
    if 'description' in node:
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


def finalize_data(input_data):
    ret = {'commands': {}}
    command_buffer = ret['commands']

    for node in input_data:
        _process_node(command_buffer, node, ret)
    return ret
