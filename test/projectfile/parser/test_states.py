#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects.projectfile import error
from projects.projectfile.parser import state
from test.helpers import *


class StartState(TestCase):
    def test__can_parse_version(self):
        data = {}
        line = 'from v1.2.3'
        expected = {'min-version': (1, 2, 3)}
        expected_state = state.before_commands
        next_state = state.start(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_tolerate_empty_lines(self):
        data = {}
        line1 = ''
        line2 = 'from v1.2.3'

        expected1 = {}
        expected2 = {'min-version': (1, 2, 3)}
        expected_state1 = state.start
        expected_state2 = state.before_commands

        next_state1 = state.start(data, line1)
        self.assertEqual(expected1, data)
        self.assertEqual(expected_state1, next_state1)

        next_state2 = state.start(data, line2)
        self.assertEqual(expected2, data)
        self.assertEqual(expected_state2, next_state2)

    def test__cannot_tolerate_anything_else(self):
        data = {}
        line = 'valami'
        with self.assertRaises(Exception) as cm:
            state.start(data, line)
        assert_exception(self, cm, SyntaxError, error.VERSION_MISSING_ERROR)

    def test__raise_error_on_invalid_version(self):
        data = {}
        line = 'from v.1'
        with self.assertRaises(Exception) as cm:
            state.start(data, line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)


class BeforeCommandsState(TestCase):
    def test__can_tolerate_empty_lines(self):
        data = {}
        line = ''
        expected = {}
        expected_state = state.before_commands
        next_state = state.before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_comments(self):
        data = {}
        line = '"""'
        expected = {}
        expected_state = state.main_comment
        next_state = state.before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_variables(self):
        data = {}
        line = 'some_variable = 42'
        expected = {'variables': {'some_variable': '42'}}
        expected_state = state.variables
        next_state = state.before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_command_header(self):
        data = {}
        line = 'my_command:'
        expected = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        expected_state = state.command
        next_state = state.before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__invalid_variable__raises_error(self):
        data = {}
        line = '  invalid_variable=4'
        with self.assertRaises(Exception) as cm:
            state.before_commands(data, line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_INDENTATION_ERROR)

    def test__invalid_command_header__raises_error(self):
        data = {}
        line = '  invalid_command|:'
        with self.assertRaises(Exception) as cm:
            state.before_commands(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INDENTATION_ERROR)

    def test__indented_line_raises_error(self):
        data = {}
        line = '  indented line'
        with self.assertRaises(Exception) as cm:
            state.before_commands(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)


class MainCommentState(TestCase):
    def test__first_comment_line_added_right(self):
        data = {}
        line = 'This is the first line for the main comment..'
        expected = {'description': line}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__another_line_appended_with_a_space_to_the_existing_ones(self):
        data = {'description': 'Some text.'}
        line = 'This should be appended..'
        expected = {'description': 'Some text. This should be appended..'}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__extra_whitespaces_will_be_ignored(self):
        data = {'description': 'Some text.'}
        line = '         \t\tThis should be appended..    \t   '
        expected = {'description': 'Some text. This should be appended..'}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__empty_line_acts_as_a_separator__appends_two_lines_to_the_end(self):
        data = {'description': 'Some text.'}
        line = ''
        expected = {'description': 'Some text.\n\n'}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__second_empty_line_does_not_add_more_seaprators(self):
        data = {'description': 'Some text.\n\n'}
        line = ''
        expected = {'description': 'Some text.\n\n'}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__next_not_empty_line_appended_nicely(self):
        data = {'description': 'Some text.\n\n'}
        line = 'vmi'
        expected = {'description': 'Some text.\n\nvmi'}
        expected_state = state.main_comment
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__comment_delimiter_ends_the_comment_capturing(self):
        data = {'description': 'Some text.\n\n'}
        line = '"""'
        expected = {'description': 'Some text.\n\n'}
        expected_state = state.variables
        next_state = state.main_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)


class VariableState(TestCase):
    def test__no_variable_parsed_yet__create_the_variable_key(self):
        data = {}
        line = 'my-variable = 42'
        expected = {'variables': {'my-variable': '42'}}
        expected_state = state.variables
        next_state = state.variables(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__next_variable_is_added_to_the_dictionary(self):
        data = {'variables': {
            'first-variable': '42'
        }}
        line = 'second-variable = 23'
        expected = {'variables': {
            'first-variable': '42',
            'second-variable': '23'
        }}
        expected_state = state.variables
        next_state = state.variables(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_tolerate_empty_lines(self):
        data = {}
        line = ''
        expected = {}
        expected_state = state.variables
        next_state = state.variables(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__invalid_variable_syntax__raises_exception(self):
        data = {}
        line = 'some-variable = \'23'
        with self.assertRaises(Exception) as cm:
            state.variables(data, line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_AFTER_ERROR)

    def test__non_variable__raises_invalid_command_header_exception(self):
        # command headers are in higher priority than variables
        data = {'variables': {
            'first-variable': '42'
        }}
        line = ' non-variable'
        with self.assertRaises(Exception) as cm:
            state.variables(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)

    def test__comment_delimiter__raises_exception(self):
        data = {'variables': {
            'first-variable': '42'
        }}
        line = '"""'
        with self.assertRaises(Exception) as cm:
            state.variables(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMENT_DELIMITER_UNEXPECTED_ERROR)

    def test__valid_command_header_switches_state(self):
        data = {'variables': {
            'first-variable': '42'
        }}
        line = 'my_command:'
        expected = {
            'variables': {
                'first-variable': '42'
            },
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        expected_state = state.command
        next_state = state.variables(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)


class CommandState(TestCase):
    def test__can_tolerate_empty_line(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = ''
        expected = dict(data)
        expected_state = state.command
        next_state = state.command(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_comment_delimiter(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = '"""'
        expected = dict(data)
        expected_state = state.command_comment
        next_state = state.command(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__indented_line__will_be_the_first_pre_command(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = '  cd ~ '
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': [
                        'cd ~'
                    ]
                }
            }
        }
        expected_state = state.pre
        next_state = state.command(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__command_separator_switches_right_to_post(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = '  ==='
        expected = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        expected_state = state.post
        next_state = state.command(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__nonindented_line__raises_exception(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = 'something'
        with self.assertRaises(Exception) as cm:
            state.command(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_UNEXPECTED_UNINDENTED_ERROR)


class CommandCommentState(TestCase):
    def test__first_comment_line_added_right(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = 'This is the first line for the main comment..'
        expected = {
            'commands': {
                'my_command': {
                    'description': 'This is the first line for the main comment..',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__another_line_appended_with_a_space_to_the_existing_ones(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text..',
                    'done': False
                }
            }
        }
        line = 'This should be appended..'
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.. This should be appended..',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__extra_whitespaces_will_be_ignored(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text..',
                    'done': False
                }
            }
        }
        line = '         \t\tThis should be appended..    \t   '
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.. This should be appended..',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__empty_line_acts_as_a_separator__appends_two_lines_to_the_end(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text.',
                    'done': False
                }
            }
        }
        line = ''
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__second_empty_line_does_not_add_more_seaprators(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        line = ''
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__next_not_empty_line_appended_nicely(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        line = 'vmi'
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\nvmi',
                    'done': False
                }
            }
        }
        expected_state = state.command_comment
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__comment_delimiter_ends_the_comment_capturing(self):
        data = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        line = '"""'
        expected = {
            'commands': {
                'my_command': {
                    'description': 'Some text.\n\n',
                    'done': False
                }
            }
        }
        expected_state = state.pre
        next_state = state.command_comment(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)


class PreState(TestCase):
    def test__can_tolerate_empty_lines(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = ''
        expected = dict(data)
        expected_state = state.pre
        next_state = state.pre(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__indented_line_processed_as_a_command(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = '  some indented command'
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['some indented command']
                }
            }
        }
        expected_state = state.pre
        next_state = state.pre(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__comment_delimiter__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = '  """'
        with self.assertRaises(Exception) as cm:
            state.post(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMENT_DELIMITER_UNEXPECTED_ERROR)

    def test__parsed_command_appended_to_the_pre_list(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['previous command']
                }
            }
        }
        line = '  some indented command'
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': [
                        'previous command',
                        'some indented command'
                    ]
                }
            }
        }
        expected_state = state.pre
        next_state = state.pre(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__command_divisor_switches_state(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['previous command']
                }
            }
        }
        line = '  ==='
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['previous command']
                }
            }
        }
        expected_state = state.post
        next_state = state.pre(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__valid_command_header_finishes_command(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['previous command']
                }
            }
        }
        line = 'next_command:'
        expected = {
            'commands': {
                'my_command': {
                    'done': True,
                    'pre': ['previous command']
                },
                'next_command': {
                    'done': False,
                }
            }
        }
        expected_state = state.command
        next_state = state.pre(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__invalid_command_header__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'pre': ['previous command']
                }
            }
        }
        line = 'next_command|'
        with self.assertRaises(Exception) as cm:
            state.pre(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)


class PostState(TestCase):
    def test__can_tolerate_empty_lines(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                }
            }
        }
        line = ''
        expected = dict(data)
        expected_state = state.post
        next_state = state.post(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__indented_line_processed_as_a_command(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False
                }
            }
        }
        line = '  some indented command'
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['some indented command']
                }
            }
        }
        expected_state = state.post
        next_state = state.post(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__comment_delimiter__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = '  """'
        with self.assertRaises(Exception) as cm:
            state.post(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMENT_DELIMITER_UNEXPECTED_ERROR)

    def test__parsed_command_appended_to_the_post_list(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = '  some indented command'
        expected = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': [
                        'previous command',
                        'some indented command'
                    ]
                }
            }
        }
        expected_state = state.post
        next_state = state.post(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__command_divisor__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = '==='
        with self.assertRaises(Exception) as cm:
            state.post(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_DELIMITER_UNEXPECTED_ERROR)

    def test__valid_command_header_finishes_command(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = 'next_command:'
        expected = {
            'commands': {
                'my_command': {
                    'done': True,
                    'post': ['previous command']
                },
                'next_command': {
                    'done': False,
                }
            }
        }
        expected_state = state.command
        next_state = state.post(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__invalid_command_header__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = 'next_command|'
        with self.assertRaises(Exception) as cm:
            state.post(data, line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__redefined_command_in_post__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = 'my_command:'
        with self.assertRaises(Exception) as cm:
            state.post(data, line)
        assert_exception(self, cm, SyntaxError,
                         error.COMMAND_HEADER_REDEFINED_ERROR.format('my_command'))

    def test__redefined_command_in_pre__raises_error(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['previous command']
                }
            }
        }
        line = 'my_command:'
        with self.assertRaises(Exception) as cm:
            state.pre(data, line)
        assert_exception(self, cm, SyntaxError,
                         error.COMMAND_HEADER_REDEFINED_ERROR.format('my_command'))
