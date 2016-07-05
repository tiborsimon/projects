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

from projects.doc_generator import generate_doc


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
                        'echo "hello'
                    ]
                },
                'another-command': {
                    'alternatives': ['c', 'd'],
                    'description': 'This is the command description..',
                    'script': [
                        'echo "hello'
                    ]
                }
            }
        }
        expected = '''\
================================================================================
                              P  R  O  J  E  C  T
================================================================================

 This is the main description..


another-command|c|d:

    This is the command description..


some-command|a|b: [another-command]

    This is the command description..


'''
        result = generate_doc(data, 80)
        self.assertEqual(expected, result)