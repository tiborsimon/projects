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

from projects import projectfile


class FileLoading(TestCase):

    def test__load_method_called_with_the_right_path(self):
        dummy_path = '/dummy/path'
        with mock.patch(builtin_module+'.open') as mock_open:
            projectfile._load(dummy_path)
            mock_open.assert_called_with(dummy_path, 'r')

    def test__load_method_returns_the_loaded_file_content_as_a_list_of_string(self):
        mock_open = mock.mock_open(read_data='line 1\nline 2')
        expected = ['line 1', 'line 2']
        with mock.patch(builtin_module+'.open', mock_open):
            result = projectfile._load('...')
            self.assertEqual(expected, result)


class VersionParser(TestCase):

    def test__valid_version_can_be_parsed_1(self):
        line = 'from v1.2.3'
        expected = (1, 2, 3)
        result = projectfile._parse_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_2(self):
        line = 'from 1.2.3'
        expected = (1, 2, 3)
        result = projectfile._parse_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_3(self):
        line = 'from           v1.2.3    '
        expected = (1, 2, 3)
        result = projectfile._parse_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_4(self):
        line = 'from v123456789.23456789.3456789'
        expected = (123456789, 23456789, 3456789)
        result = projectfile._parse_version(line)
        self.assertEqual(expected, result)

    def test__invalid_version__raise_exception_1(self):
        line = ' from v1.2.3'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_version__raise_exception_2(self):
        line = '       from v1.2.3'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_version__raise_exception_3(self):
        line = '\t\tfrom v1.2.3'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_version__raise_exception_4(self):
        line = 'from v1.2'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_FORMAT_ERROR == cm.exception.args[0])

    def test__invalid_version__raise_exception_5(self):
        line = 'from v1.2_4'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_FORMAT_ERROR == cm.exception.args[0])

    def test__not_version_related_input__returns_none(self):
        line = 'something'
        expected = None
        result = projectfile._parse_version(line)
        self.assertEqual(expected, result)


class LineParser(TestCase):

    def test__line_can_be_parsed_1(self):
        line = 'valami'
        expected = 'valami'
        result = projectfile._parse_line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_2(self):
        line = ' valami'
        expected = 'valami'
        result = projectfile._parse_line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_3(self):
        line = '   valami    '
        expected = 'valami'
        result = projectfile._parse_line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_4(self):
        line = '\t\tvalami    '
        expected = 'valami'
        result = projectfile._parse_line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_5(self):
        line = ' valami valami    '
        expected = 'valami valami'
        result = projectfile._parse_line(line)
        self.assertEqual(expected, result)


class EmptyLineParser(TestCase):

    def test__parse_empty_line_1(self):
        line = ''
        expected = True
        result = projectfile._parse_empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_2(self):
        line = ' '
        expected = True
        result = projectfile._parse_empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_3(self):
        line = '\t'
        expected = True
        result = projectfile._parse_empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_4(self):
        line = 'valami'
        expected = False
        result = projectfile._parse_empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_5(self):
        line = '  valami'
        expected = False
        result = projectfile._parse_empty_line(line)
        self.assertEqual(expected, result)


class IndentedLineParser(TestCase):

    def test__parse_indented_line_1(self):
        line = ' valami'
        expected = 'valami'
        result = projectfile._parse_indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_2(self):
        line = '           valami'
        expected = 'valami'
        result = projectfile._parse_indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_3(self):
        line = ' valami valamik    '
        expected = 'valami valamik'
        result = projectfile._parse_indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_4(self):
        line = 'valami'
        expected = None
        result = projectfile._parse_indented_line(line)
        self.assertEqual(expected, result)


class CommentDelimiterParser(TestCase):

    def test__comment_delimiter_can_be_parsed_1(self):
        line = '"""'
        expected = True
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_2(self):
        line = '  """'
        expected = True
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_3(self):
        line = '\t"""'
        expected = True
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_4(self):
        line = '   """     '
        expected = True
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_5(self):
        line = '""'
        expected = False
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_6(self):
        line = '" ""'
        expected = False
        result = projectfile._parse_comment_delimiter(line)
        self.assertEqual(expected, result)


class VariableParser(TestCase):

    def test__variable_can_be_parsed__basic_case(self):
        line = 'my_variable = valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__more_whitespaces(self):
        line = 'my_variable   =   valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_whitespace(self):
        line = 'my_variable=valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value(self):
        line = 'my_variable = valami vmi'
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value_and_after_value(self):
        line = 'my_variable = valami vmi     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value(self):
        line = 'my_variable = "valami vmi"'
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_tailing_whitespace(self):
        line = 'my_variable = "valami vmi"     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = "valami\\"vmi"'
        expected = {'my_variable': 'valami"vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_quote(self):
        line = 'my_variable = "valami\\\'vmi"'
        expected = {'my_variable': 'valami\'vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value(self):
        line = 'my_variable = \'valami vmi\''
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_tailing_whitespace(self):
        line = 'my_variable = \'valami vmi\'     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = \'valami\\"vmi\''
        expected = {'my_variable': 'valami"vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_quote(self):
        line = 'my_variable = \'valami\\\'vmi\''
        expected = {'my_variable': 'valami\'vmi'}
        result = projectfile._parse_variable(line)
        self.assertEqual(expected, result)

    def test__invalid_variable__indentation_should_raise_exception__basic_case(self):
        line = ' my_variable = valami'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__more_whitespaces(self):
        line = '         my_variable = valami'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__tabs(self):
        line = '\t\tmy_variable = valami'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__should_raise_exception__unmatched_quote_1(self):
        line = 'my_variable = \'valami'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_AFTER_ERROR == cm.exception.args[0])

    def test__invalid_variable__should_raise_exception__unmatched_quote_2(self):
        line = 'my_variable = valami\''
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_BEFORE_ERROR == cm.exception.args[0])

    def test__invalid_variable__should_raise_exception__unmatched_double_quote_1(self):
        line = 'my_variable = "valami'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_AFTER_ERROR == cm.exception.args[0])

    def test__invalid_variable__should_raise_exception__unmatched_double_quote_2(self):
        line = 'my_variable = valami"'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_BEFORE_ERROR == cm.exception.args[0])


class CommandDivisorParser(TestCase):

    def test__command_divisor_can_be_parsed_1(self):
        line = '==='
        expected = True
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_2(self):
        line = ' ==='
        expected = True
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_3(self):
        line = ' ===      '
        expected = True
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_4(self):
        line = '\t==='
        expected = True
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_5(self):
        line = '=='
        expected = False
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_6(self):
        line = '='
        expected = False
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_7(self):
        line = '= =='
        expected = False
        result = projectfile._parse_command_divisor(line)
        self.assertEqual(expected, result)


class CommandHeaderParser(TestCase):

    def test__valid_command_header__basic_case(self):
        line = 'command:'
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__command_name_full_range(self):
        line = 'command_COMMAND_1234567890.abc-abc:'
        expected = {
            'command_COMMAND_1234567890.abc-abc': {
                'dependencies': [],
                'done': False
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_after_colon(self):
        line = 'command:   '
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_before_colon(self):
        line = 'command  :'
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__two_alternative_commands(self):
        line = 'command|com:'
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            },
            'com': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__three_alternative_commands(self):
        line = 'command|com|c:'
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__alternatives_with_space(self):
        line = 'command |  com    | c    :'
        expected = {
            'command': {
                'dependencies': [],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies(self):
        line = 'command|com|c: [dep]'
        expected = {
            'command': {
                'dependencies': ['dep'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__multiple_dependencies(self):
        line = 'command|com|c: [dep, dep2, dep3]'
        expected = {
            'command': {
                'dependencies': ['dep', 'dep2', 'dep3'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__full_range_dependencies(self):
        line = 'command|com|c: [command_COMMAND_1234567890.abc-abc]'
        expected = {
            'command': {
                'dependencies': ['command_COMMAND_1234567890.abc-abc'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_no_whitespaces(self):
        line = 'command|com|c:[dep]'
        expected = {
            'command': {
                'dependencies': ['dep'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_more_outside_whitespaces(self):
        line = 'command|com|c:    [dep]          '
        expected = {
            'command': {
                'dependencies': ['dep'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep    ]'
        expected = {
            'command': {
                'dependencies': ['dep'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__multiple_dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep  ,               dep1  ]'
        expected = {
            'command': {
                'dependencies': ['dep', 'dep1'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = projectfile._parse_command_header(line)
        self.assertEqual(expected, result)

    def test__invalid_command_header__raises_exception__indentation_1(self):
        line = ' command'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__indentation_2(self):
        line = '     command'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__indentation_3(self):
        line = '\tcommand'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_1(self):
        line = 'command'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_2(self):
        line = 'command|'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_3(self):
        line = 'command   [deb]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_1(self):
        line = 'command:c'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_2(self):
        line = ':command'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_1(self):
        line = 'command|:'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_2(self):
        line = '|command:'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_3(self):
        line = '|command|:'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_4(self):
        line = 'command||:'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_1(self):
        line = 'command: []'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_EMPTY_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_2(self):
        line = 'command: ['
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_3(self):
        line = 'command: ]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_4(self):
        line = 'command: [,]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_5(self):
        line = 'command: [ ,]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_6(self):
        line = 'command: [ ,  ]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_7(self):
        line = 'command: [dep1, , dep2]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_8(self):
        line = 'command: [dep1,,dep2]'
        with self.assertRaises(Exception) as cm:
            projectfile._parse_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])


class StartState(TestCase):

    def test__can_parse_version(self):
        data = {}
        line = 'from v1.2.3'
        expected = {'min-version': (1, 2, 3)}
        expected_state = projectfile._state_before_commands
        next_state = projectfile._state_start(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_tolerate_empty_lines(self):
        data = {}
        line1 = ''
        line2 = 'from v1.2.3'

        expected1 = {}
        expected2 = {'min-version': (1, 2, 3)}
        expected_state1 = projectfile._state_start
        expected_state2 = projectfile._state_before_commands

        next_state1 = projectfile._state_start(data, line1)
        self.assertEqual(expected1, data)
        self.assertEqual(expected_state1, next_state1)

        next_state2 = projectfile._state_start(data, line2)
        self.assertEqual(expected2, data)
        self.assertEqual(expected_state2, next_state2)

    def test__cannot_tolerate_anything_else(self):
        data = {}
        line = 'valami'
        with self.assertRaises(Exception) as cm:
            projectfile._state_start(data, line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_MISSING_ERROR == cm.exception.args[0])

    def test__raise_error_on_invalid_version(self):
        data = {}
        line = 'from v.1'
        with self.assertRaises(Exception) as cm:
            projectfile._state_start(data, line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_FORMAT_ERROR == cm.exception.args[0])


class BeforeCommandsState(TestCase):

    def test__can_tolerate_empty_lines(self):
        data = {}
        line = ''
        expected = {}
        expected_state = projectfile._state_before_commands
        next_state = projectfile._state_before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_comments(self):
        data = {}
        line = '"""'
        expected = {'description': {'done': False}}
        expected_state = projectfile._state_main_comment
        next_state = projectfile._state_before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_variables(self):
        data = {}
        line = 'some_variable = 42'
        expected = {'variables': {'some_variable': '42'}}
        expected_state = projectfile._state_variables
        next_state = projectfile._state_before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)

    def test__can_parse_command_header(self):
        data = {}
        line = 'my_command:'
        expected = {
            'commands': {
                'my_command': {
                    'dependencies': [],
                    'done': False
                }
            }
        }
        expected_state = projectfile._state_command
        next_state = projectfile._state_before_commands(data, line)
        self.assertEqual(expected, data)
        self.assertEqual(expected_state, next_state)


