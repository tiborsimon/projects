#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
try:
    import mock
except ImportError:
    from unittest import mock

from projects import main


class DetermineIfCallHappenedFromProject(TestCase):
    @mock.patch.object(main, 'execute_call', autospec=True)
    def test__simple_command_can_be_executed_regardless_of_extra_whitespaces(self, mock_execute_call):
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
        concatenated_commands = ' && '.join(data['commands']['command']['script'])
        calls = [
            mock.call(concatenated_commands)
        ]
        mock_execute_call.return_value = ('', '')
        main.execute(args, data, {'doc-width': 80})
        mock_execute_call.assert_has_calls(calls)

    @mock.patch.object(main, 'execute_call', autospec=True)
    def test__alias_can_be_redirected(self, mock_execute_call):
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
        concatenated_commands = ' && '.join(data['commands']['command']['script'])
        calls = [
            mock.call(concatenated_commands)
        ]
        mock_execute_call.return_value = ('', '')
        main.execute(args, data, {'doc-width': 80})
        mock_execute_call.assert_has_calls(calls)

    @mock.patch.object(main, 'execute_call', autospec=True)
    def test__dependencies_can_be_handled(self, mock_execute_call):
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
        concatenated_commands1 = ' && '.join(data['commands']['command1']['script'])
        concatenated_commands2 = ' && '.join(data['commands']['command2']['script'])
        calls = [
            mock.call(concatenated_commands1),
            mock.call(concatenated_commands2)
        ]
        mock_execute_call.return_value = ('', '')
        main.execute(args, data, {'doc-width': 80})
        mock_execute_call.assert_has_calls(calls)

    @mock.patch.object(main, 'execute_call', autospec=True)
    def test__two_dependencies_with_multiple_aliases(self, mock_execute_call):
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
        concatenated_commands1 = ' && '.join(data['commands']['command1']['script'])
        concatenated_commands2 = ' && '.join(data['commands']['command2']['script'])
        concatenated_commands3 = ' && '.join(data['commands']['command3']['script'])
        concatenated_commands4 = ' && '.join(data['commands']['command4']['script'])
        calls = [
            mock.call(concatenated_commands4),
            mock.call(concatenated_commands3),
            mock.call(concatenated_commands2),
            mock.call(concatenated_commands1)
        ]
        mock_execute_call.return_value = ('', '')
        main.execute(args, data, {'doc-width': 80})
        mock_execute_call.assert_has_calls(calls)


