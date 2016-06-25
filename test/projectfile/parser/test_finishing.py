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

from test.helpers import *

from projects.projectfile import error
from projects.projectfile.parser import state
from projects.projectfile import parser

class FinishingState(TestCase):
    def test__eof_in_pre_state__data_will_be_closed(self):
        s = state.pre
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['some command']
                }
            }
        }
        expected = {
            'commands': {
                'my_command': {
                    'pre': ['some command']
                }
            }
        }
        parser._finish_processing(data, s)
        self.assertEqual(expected, data)

    def test__eof_in_post_state__data_will_be_closed(self):
        s = state.post
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['some command']
                }
            }
        }
        expected = {
            'commands': {
                'my_command': {
                    'post': ['some command']
                }
            }
        }
        parser._finish_processing(data, s)
        self.assertEqual(expected, data)

    def test__alternative_commands_can_be_handled_by_the_finalizer(self):
        s = state.post
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['some command']
                },
                'alternative': {
                    'alias': 'my_command'
                }
            }
        }
        expected = {
            'commands': {
                'my_command': {
                    'post': ['some command']
                },
                'alternative': {
                    'alias': 'my_command'
                }
            }
        }
        parser._finish_processing(data, s)
        self.assertEqual(expected, data)

    def test__eof_in_start_state__raises_error(self):
        data = {}
        s = state.start
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError, error.PROJECTFILE_EMPTY_ERROR)

    def test__eof_in_before_commands_state__raises_error(self):
        data = {}
        s = state.before_commands
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError, error.PROJECTFILE_NO_COMMAND_ERROR)

    def test__eof_in_main_comment_state__raises_error(self):
        data = {}
        s = state.main_comment
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError, error.PROJECTFILE_NO_COMMAND_ERROR)

    def test__eof_in_variable_state__raises_error(self):
        data = {}
        s = state.variables
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError, error.PROJECTFILE_NO_COMMAND_ERROR)

    def test__eof_in_command_state__raises_error(self):
        data = {
            'commands': {
                'unfinished-command': {
                    'done': False
                }
            }
        }
        s = state.command
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError,
                         error.PROJECTFILE_NO_COMMAND_IN_COMMAND_ERROR.format('unfinished-command'))

    def test__eof_in_command_comment_state__raises_error(self):
        data = {
            'commands': {
                'unfinished-command': {
                    'done': False
                }
            }
        }
        s = state.command_comment
        with self.assertRaises(Exception) as cm:
            parser._finish_processing(data, s)
        assert_exception(self, cm, SyntaxError,
                         error.PROJECTFILE_NO_COMMAND_IN_COMMAND_ERROR.format('unfinished-command'))


class DataIntegrityTest(TestCase):
    def test__dependecies_refers_to_existing_commands__raises_no_error(self):
        data = {
            'commands': {
                'c1': {},
                'c2': {
                    'dependencies': ['c1']
                }
            }
        }
        parser._data_integrity_check(data)

    def test__non_existing_dependency__raises_error(self):
        data = {
            'commands': {
                'c1': {},
                'c2': {
                    'dependencies': ['c']
                }
            }
        }
        with self.assertRaises(Exception) as cm:
            parser._data_integrity_check(data)
        assert_exception(self, cm, error.ProjectfileError,
                         {'error': error.PROJECTFILE_INVALID_DEPENDENCY.format('c', 'c2')})

    def test__dependencies_are_tansitive(self):
        data = {
            'commands': {
                'c1': {},
                'c2': {
                    'dependencies': ['c']
                },
                'c': {
                    'alias': 'c1'
                }
            }
        }
        parser._data_integrity_check(data)

class Integration(TestCase):
    @mock.patch.object(parser, '_parse_lines')
    @mock.patch.object(parser, '_data_integrity_check')
    def test__data_integrity_gets_called_by_parser(self, mock_checker, mock_parser):
        mock_parser.return_value = 'something'
        parser.process_lines(None)
        mock_checker.assert_called_with('something')
