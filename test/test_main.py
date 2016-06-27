#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
try:
    import mock
except ImportError:
    from unittest import mock

import main


class DetermineIfCallHappenedFromProject(TestCase):
    @mock.patch.object(main, 'call', autospec=True)
    def test__simple_command_can_be_executed_regardless_of_extra_whitespaces(self, mock_call):
        args = ['x', 'x', 'command']
        data = {
            'min-version': (2, 0, 0),
            'commands': {
                'command': {
                    'script': [
                        'a     a  a',
                        'b b   b'
                    ]
                }
            }
        }
        calls = [
            mock.call(['a', 'a', 'a']),
            mock.call(['b', 'b', 'b'])
        ]
        main.execute(args, data, {'doc-width': 80})
        mock_call.assert_has_calls(calls)

    @mock.patch.object(main, 'call', autospec=True)
    def test__alias_can_be_redirected(self, mock_call):
        args = ['x', 'x', 'c']
        data = {
            'min-version': (2, 0, 0),
            'commands': {
                'command': {
                    'script': [
                        'a     a  a',
                        'b b   b'
                    ]
                },
                'c': {
                    'alias': 'command'
                }
            }
        }
        calls = [
            mock.call(['a', 'a', 'a']),
            mock.call(['b', 'b', 'b'])
        ]
        main.execute(args, data, {'doc-width': 80})
        mock_call.assert_has_calls(calls)

    @mock.patch.object(main, 'call', autospec=True)
    def test__dependencies_can_be_handled(self, mock_call):
        args = ['x', 'x', 'c']
        data = {
            'min-version': (2, 0, 0),
            'commands': {
                'command1': {
                    'script': [
                        'command 1 commands'
                    ]
                },
                'command2': {
                    'dependencies': ['command1'],
                    'script': [
                        'command 2 commands'
                    ]
                },
                'c': {
                    'alias': 'command2'
                }
            }
        }
        calls = [
            mock.call(['command', '1', 'commands']),
            mock.call(['command', '2', 'commands'])
        ]
        main.execute(args, data, {'doc-width': 80})
        mock_call.assert_has_calls(calls)

    @mock.patch.object(main, 'call', autospec=True)
    def test__two_dependencies_with_multiple_aliases(self, mock_call):
        args = ['x', 'x', 'c1']
        data = {
            'min-version': (2, 0, 0),
            'commands': {
                'command1': {
                    'dependencies': ['c3', 'c2'],
                    'script': [
                        'command 1 commands'
                    ]
                },
                'command2': {
                    'script': [
                        'command 2 commands'
                    ]
                },
                'command3': {
                    'dependencies': ['command4'],
                    'script': [
                        'command 3 commands'
                    ]
                },
                'command4': {
                    'script': [
                        'command 4 commands'
                    ]
                },
                'c1': {
                    'alias': 'command1'
                },
                'c2': {
                    'alias': 'command2'
                },
                'c3': {
                    'alias': 'command3'
                }
            }
        }
        calls = [
            mock.call(['command', '4', 'commands']),
            mock.call(['command', '3', 'commands']),
            mock.call(['command', '2', 'commands']),
            mock.call(['command', '1', 'commands'])
        ]
        main.execute(args, data, {'doc-width': 80})
        mock_call.assert_has_calls(calls)


