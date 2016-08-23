#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    from unittest import mock

try:
    import __builtin__
    builtin_module = '__builtin__'
except ImportError:
    builtin_module = 'builtins'

from projects.gui.doc_generator import generate_doc, generate_markdown


class DocGeneratorTests(TestCase):
    def test__simple_data_with_one_command_can_be_processed(self):
        data = {
            'name': 'project',
            'min-version': (1, 2, 3),
            'description': 'This is the main description..',
            'commands': {
                'some-command': {
                    'alternatives': ['a', 'b'],
                    'dependencies': ['another-command'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello"'
                    ]
                },
                'another-command': {
                    'alternatives': ['c', 'd'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello"'
                    ]
                }
            }
        }
        expected = '''\
{head}================================================================================{reset}
{project}                              P  R  O  J  E  C  T{reset}
{head}================================================================================{reset}

This is the main description..


{command}another-command|c|d:{reset}

  This is the command description..


{command}some-command|a|b: [another-command]{reset}

  This is the command description..


'''
        result = generate_doc(data, 80)
        self.assertEqual(expected, result)


class MarkdownGeneration(TestCase):
    def test__simple_data_tructure_can_be_converted(self):
        data = {
            'name': 'project',
            'min-version': (1, 2, 3),
            'description': 'This is the main description..',
            'commands': {
                'some-command': {
                    'alternatives': ['a', 'b'],
                    'dependencies': ['another-command'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello"'
                    ]
                },
                'another-command': {
                    'alternatives': ['c', 'd'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello"'
                    ]
                },
                'yet-another-command': {
                    'dependencies': ['another-command'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello"'
                    ]
                },
                'alt-alt': {
                    'alias': 'something..'
                }
            }
        }
        expected = '''\
# project

This is the main description..

---

### another-command

- _alternatives_: `c`, `d`

This is the command description..

### some-command

- _alternatives_: `a`, `b`
- _dependencies_: `another-command`

This is the command description..

### yet-another-command

- _dependencies_: `another-command`

This is the command description..

'''
        result = generate_markdown(data)
        self.assertEqual(expected, result)
