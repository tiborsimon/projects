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
    ret = {}
    node = input_data[0]
    command_names = list(node['commands'].keys())
    commands = {}
    for c in command_names:
        command = node['commands'][c]
        commands[c] = {
            'script': []
        }
        commands[c]['script'].append('cd ' + node['path'])
        commands[c]['script'].extend(command['pre'])
        if 'post' in command:
            commands[c]['script'].extend(command['post'])

    ret['min-version'] = node['min-version']
    ret['commands'] = commands
    if 'description' in node:
        ret['description'] = node['description']

    return ret
