#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from . import error


def generate_command_tree(processing_tree):
    ret = {'commands': {}}
    command_buffer = ret['commands']
    for node in processing_tree:
        process_commands(command_buffer, node)
        add_version(ret, node)
        add_variables(ret, node)
        add_description(ret, node)
    remove_helper_values(command_buffer)
    return ret


def process_commands(command_buffer, node):
    for command_name in node['commands']:
        pool = get_pool(command_buffer, command_name, node)
        if pool is not None:
            add_path(node, pool)
            add_alternatives(command_name, node, command_buffer)
            add_command_description(command_name, node, command_buffer)
            add_dependency(command_name, node, command_buffer)
            add_pre(command_name, node, pool)
            add_post(command_name, node, pool)


def add_path(node, pool):
    pool['path'] = node['path']


def add_command_description(command_name, node, command_buffer):
    if 'description' in node['commands'][command_name]:
        if 'description' in command_buffer[command_name]:
            command_buffer[command_name]['description'] += '\n\n' + node['commands'][command_name]['description']
        else:
            command_buffer[command_name]['description'] = node['commands'][command_name]['description']


def add_dependency(command_name, node, command_buffer):
    if 'dependencies' in node['commands'][command_name]:
        if 'dependencies' in command_buffer[command_name]:
            for dep in node['commands'][command_name]['dependencies']:
                if dep not in command_buffer[command_name]['dependencies']:
                    command_buffer[command_name]['dependencies'].append(dep)
        else:
            command_buffer[command_name]['dependencies'] = node['commands'][command_name]['dependencies']


def add_alternatives(command_name, node, command_buffer):
    if 'alternatives' in node['commands'][command_name]:
        if 'alternatives' in command_buffer[command_name]:
            for alt in node['commands'][command_name]['alternatives']:
                if alt not in command_buffer[command_name]['alternatives']:
                    command_buffer[command_name]['alternatives'].extend([alt])
            command_buffer[command_name]['alternatives'].sort(key=len, reverse=True)
        else:
            command_buffer[command_name]['alternatives'] = node['commands'][command_name]['alternatives']


def add_pre(command_name, node, pool):
    if 'pre' in node['commands'][command_name]:
        pool['pre'] = node['commands'][command_name]['pre']


def add_post(command_name, node, pool):
    if 'post' in node['commands'][command_name]:
        pool['post'] = node['commands'][command_name]['post']


def add_version(data, node):
    if 'min-version' in data:
        if data['min-version'] > node['min-version']:
            data['min-version'] = node['min-version']
    else:
        data['min-version'] = node['min-version']


def add_variables(data, node):
    if 'variables' in node:
        if 'variables' not in data:
            data['variables'] = {}
        for var in node['variables']:
            if var in data['variables']:
                raise error.ProjectfileError({
                    'error': error.VARIABLE_REDEFINED_ERROR.format(var, data['variables'][var]['path'], node['path']),
                    'path': node['path']
                })
            else:
                data['variables'][var] = {
                    'value': node['variables'][var],
                    'path': node['path']
                }


def add_description(data, node):
    if 'description' in node:
        if 'description' in data:
            data['description'] += '\n\n' + node['description']
        else:
            data['description'] = node['description']


def remove_helper_values(command_buffer):
    for command_name in command_buffer:
        if 'stack' in command_buffer[command_name]:
            del command_buffer[command_name]['stack']


def get_pool(command_buffer, command_name, node):
    if command_name not in command_buffer:
        if 'alias' in node['commands'][command_name]:
            command_buffer[command_name] = {
                'alias': node['commands'][command_name]['alias']
            }
            return None
        else:
            command_buffer[command_name] = {
                'root': [{}]
            }
            reset_stack(command_buffer, command_name)
    else:
        if 'alias' in node['commands'][command_name]:
            already_aliased_name = command_buffer[command_name]['alias']
            newly_aliased_name = node['commands'][command_name]['alias']
            if newly_aliased_name != already_aliased_name:
                raise error.ProjectfileError({
                    'error': error.PROJECTFILE_ALTERNATIVE_REDEFINED.format(command_name, already_aliased_name, newly_aliased_name)
                })
            return None
        if 'alias' in command_buffer[command_name]:
            command_name = command_buffer[command_name]['alias']
        stack = command_buffer[command_name]['stack']
        while stack and not node['path'].startswith(stack[-1][-1]['path']):
            stack.pop()
        if not stack:
            reset_stack(command_buffer, command_name)
            command_buffer[command_name]['stack'][-1].append({})
        else:
            if 'children' in stack[-1][-1]:
                stack[-1][-1]['children'].append({})
            else:
                stack[-1][-1]['children'] = [{}]
            stack = stack[-1][-1]['children']
            command_buffer[command_name]['stack'].append(stack)
    return command_buffer[command_name]['stack'][-1][-1]


def reset_stack(command_buffer, command_name):
    command_buffer[command_name]['stack'] = [command_buffer[command_name]['root']]


def substitute_variables(line, variables):
    for var_name in variables:
        line = line.replace('$' + var_name, variables[var_name]['value'])
        line = line.replace('${' + var_name + '}', variables[var_name]['value'])
    return line


def process_variables(data):
    if 'variables' in data:
        for command_name in data['commands']:
            command = data['commands'][command_name]
            if 'alias' in command:
                continue
            _apply_variables_to_command_description(command, data)
            _apply_variables_to_command_lines(command, data)
        _apply_variables_to_main_description(data)
        del data['variables']


def _apply_variables_to_command_description(command, data):
    if 'description' in command:
        command['description'] = substitute_variables(command['description'], data['variables'])


def _apply_variables_to_command_lines(command, data):
    temp_lines = []
    for line in command['script']:
        line = substitute_variables(line, data['variables'])
        temp_lines.append(line)
    command['script'] = temp_lines


def _apply_variables_to_main_description(data):
    if 'description' in data:
        data['description'] = substitute_variables(data['description'], data['variables'])


def flatten_node(script, node):
    append_path(node, script)
    if 'pre' in node:
        for line in node['pre']:
            script.append(line)
    if 'children' in node:
        for child in node['children']:
            flatten_node(script, child)
            if 'post' in node:
                append_path(node, script)
    if 'post' in node:
        for line in node['post']:
            script.append(line)


def append_path(node, script):
    if script and script[-1].startswith('cd'):
        script.pop()
    script.append('cd {}'.format(node['path']))


def flatten_commands(command_tree):
    for command_name in command_tree['commands']:
        command = command_tree['commands'][command_name]
        if 'alias' in command:
            continue
        script = []
        for node in command['root']:
            flatten_node(script, node)
        command['script'] = script
        del command['root']
