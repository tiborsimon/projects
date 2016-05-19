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
    for path, lines in file_handler.projectfile_walk(project_root):
        temp = {
            'path': path,
            'data': parser.process_lines(lines),
            'children': []
        }
        while stack and not path.startswith(stack[-1]['path']):
            stack.pop()
        if stack:
            stack[-1]['children'].append(temp)
        else:
            ret.append(temp)
            stack = [temp]
        stack.append(temp)
    return ret


def finalize_data(input_data):
    commands = input_data[0]['data']['commands'].keys()
    ret = {
        'min-version': input_data[0]['data']['min-version'],
        'commands': {
            commands[0]: ['cd ' + input_data[0]['path']] + input_data[0]['data']['commands'][commands[0]]['pre']
        }
    }
    return ret