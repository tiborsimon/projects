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
        main.execute(args, data)
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
        main.execute(args, data)
        mock_call.assert_has_calls(calls)


