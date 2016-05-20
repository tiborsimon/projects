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


def finalize_data(input_data):
    def get_current_command(_command_name, _commands, _node):
        command = _node['commands'][_command_name]
        if _command_name not in _commands:
            _commands[_command_name] = {'script': []}
        return command

    def add_cd(_command_name, _commands, _node):
        _commands[_command_name]['script'].append('cd ' + _node['path'])

    def add_pre(_command_name, _command, _commands):
        _commands[_command_name]['script'].extend(_command['pre'])

    def add_post(_command_name, _command, _commands):
        if 'post' in _command:
            _commands[_command_name]['script'].extend(_command['post'])

    def add_command_description(_command_name, _command, _commands):
        if 'description' in _command:
            _commands[_command_name]['description'] = _command['description']

    def add_version(_node, _ret):
        _ret['min-version'] = _node['min-version']

    def add_main_description(_node, _ret):
        if 'description' in _node:
            _ret['description'] = _node['description']

    def command_names(_node):
        return list(_node['commands'].keys())

    def process_children(_command_name, _commands, _node):
        for child in _node['children']:
            if _command_name in child['commands']:
                process_command(_command_name, _commands, child)
            else:
                process_children(_command_name, _commands, child)

    def process_command(_command_name, _commands, _node):
        command = get_current_command(_command_name, _commands, _node)
        add_command_description(_command_name, command, _commands)
        add_cd(_command_name, _commands, _node)
        add_pre(_command_name, command, _commands)
        process_children(_command_name, _commands, _node)
        add_post(_command_name, command, _commands)

    ret = {'commands': {}}

    commands = ret['commands']
    for node in input_data:
        for command_name in command_names(node):
            process_command(command_name, commands, node)
        add_version(node, ret)
        add_main_description(node, ret)
    return ret

