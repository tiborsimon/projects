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
    ret = []
    stack = []

    def pop_stack_until_common_node(s, p):
        while s and not p.startswith(s[-1]['path']):
            s.pop()

    def chain_data_to_last_element(s, t):
        s[-1]['children'].append(t)
        s.append(t)

    def initialize_stack(r, t):
        r.append(t)
        return [t]

    for path, lines in file_handler.projectfile_walk(project_root):
        temp = {
            'path': path,
            'data': parser.process_lines(lines),
            'children': []
        }
        pop_stack_until_common_node(stack, path)
        if stack:
            chain_data_to_last_element(stack, temp)
        else:
            stack = initialize_stack(ret, temp)
    return ret


def finalize_data(input_data):
    commands = list(input_data[0]['data']['commands'].keys())
    ret = {
        'min-version': input_data[0]['data']['min-version'],
        'commands': {
            commands[0]: ['cd ' + input_data[0]['path']] + input_data[0]['data']['commands'][commands[0]]['pre']
        }
    }
    return ret
