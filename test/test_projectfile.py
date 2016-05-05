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
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_2(self):
        line = 'from 1.2.3'
        expected = (1, 2, 3)
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_3(self):
        line = 'from           v1.2.3    '
        expected = (1, 2, 3)
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_parser_for_invalid_version__returns_none_1(self):
        line = 'fromv1.2.3'
        expected = None
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_parser_for_invalid_version__returns_none_2(self):
        line = ' from v1.2.3'
        expected = None
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__valid_version_parser_for_invalid_version__returns_none_3(self):
        line = 'from v1.2'
        expected = None
        result = projectfile._valid_version(line)
        self.assertEqual(expected, result)

    def test__invalid_version__raise_exception_1(self):
        line = ' from v1.2.3'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_version__raise_exception_2(self):
        line = 'from v1.2'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VERSION_FORMAT_ERROR == cm.exception.args[0])

    def test__double_check_invalid_version_with_valid_string(self):
        line = 'from v1.2.3'
        expected = None
        result = projectfile._invalid_version(line)
        self.assertEqual(expected, result)

class LineParser(TestCase):

    def test__line_can_be_parsed_1(self):
        line = 'valami'
        expected = 'valami'
        result = projectfile._line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_2(self):
        line = ' valami'
        expected = 'valami'
        result = projectfile._line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_3(self):
        line = '   valami    '
        expected = 'valami'
        result = projectfile._line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_4(self):
        line = '\t\tvalami    '
        expected = 'valami'
        result = projectfile._line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_5(self):
        line = ' valami valami    '
        expected = 'valami valami'
        result = projectfile._line(line)
        self.assertEqual(expected, result)


class EmptyLineParser(TestCase):

    def test__parse_empty_line_1(self):
        line = ''
        expected = True
        result = projectfile._empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_2(self):
        line = ' '
        expected = True
        result = projectfile._empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_3(self):
        line = '\t'
        expected = True
        result = projectfile._empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_4(self):
        line = 'valami'
        expected = False
        result = projectfile._empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_5(self):
        line = '  valami'
        expected = False
        result = projectfile._empty_line(line)
        self.assertEqual(expected, result)


class IndentedLineParser(TestCase):

    def test__parse_indented_line_1(self):
        line = ' valami'
        expected = 'valami'
        result = projectfile._indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_2(self):
        line = '           valami'
        expected = 'valami'
        result = projectfile._indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_3(self):
        line = ' valami valamik    '
        expected = 'valami valamik'
        result = projectfile._indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_4(self):
        line = 'valami'
        expected = None
        result = projectfile._indented_line(line)
        self.assertEqual(expected, result)


class CommentDelimiterParser(TestCase):

    def test__comment_delimiter_can_be_parsed_1(self):
        line = '"""'
        expected = True
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_2(self):
        line = '  """'
        expected = True
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_3(self):
        line = '\t"""'
        expected = True
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_4(self):
        line = '   """     '
        expected = True
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_5(self):
        line = '""'
        expected = False
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__comment_delimiter_can_be_parsed_6(self):
        line = '" ""'
        expected = False
        result = projectfile._comment_delimiter(line)
        self.assertEqual(expected, result)


class VariableParser(TestCase):

    def test__variable_can_be_parsed__basic_case(self):
        line = 'my_variable = valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__more_whitespaces(self):
        line = 'my_variable   =   valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_whitespace(self):
        line = 'my_variable=valami'
        expected = {'my_variable': 'valami'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value(self):
        line = 'my_variable = valami vmi'
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value_and_after_value(self):
        line = 'my_variable = valami vmi     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value(self):
        line = 'my_variable = "valami vmi"'
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_tailing_whitespace(self):
        line = 'my_variable = "valami vmi"     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = "valami\\"vmi"'
        expected = {'my_variable': 'valami"vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_quote(self):
        line = 'my_variable = "valami\\\'vmi"'
        expected = {'my_variable': 'valami\'vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value(self):
        line = 'my_variable = \'valami vmi\''
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_tailing_whitespace(self):
        line = 'my_variable = \'valami vmi\'     '
        expected = {'my_variable': 'valami vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = \'valami\\"vmi\''
        expected = {'my_variable': 'valami"vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_quote(self):
        line = 'my_variable = \'valami\\\'vmi\''
        expected = {'my_variable': 'valami\'vmi'}
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__leading_whitespace__returns_none(self):
        line = ' my_variable = valami'
        expected = None
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_matching_quote__returns_none_1(self):
        line = 'my_variable = "valami'
        expected = None
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_matching_quote__returns_none_2(self):
        line = 'my_variable = \'valami'
        expected = None
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_matching_quote__returns_none_3(self):
        line = 'my_variable = valami"'
        expected = None
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_matching_quote__returns_none_4(self):
        line = 'my_variable = valami\''
        expected = None
        result = projectfile._valid_variable(line)
        self.assertEqual(expected, result)

    def test__invalid_variable__indentation_should_raise_exception__basic_case(self):
        line = ' my_variable = valami'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__more_whitespaces(self):
        line = '         my_variable = valami'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__quoted_value(self):
        line = ' my_variable = \'valami\''
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__double_quoted_value(self):
        line = '  my_variable = "valami"'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__quoted_value_with_escaped_quote(self):
        line = ' my_variable = \'valami\\\'vmi\''
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__quoted_value_with_escaped_double_quote(self):
        line = ' my_variable = \'valami\"vmi\''
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__double_quoted_value_with_escaped_quote(self):
        line = ' my_variable = "valami\\\'vmi"'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__double_quoted_value_with_escaped_double_quote(self):
        line = ' my_variable = "valami\"vmi"'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__unmatched_quote_1(self):
        line = 'my_variable = \'valami'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_AFTER_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__unmatched_quote_2(self):
        line = 'my_variable = valami\''
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_BEFORE_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__unmatched_double_quote_1(self):
        line = 'my_variable = "valami'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_AFTER_ERROR == cm.exception.args[0])

    def test__invalid_variable__indentation_should_raise_exception__unmatched_double_quote_2(self):
        line = 'my_variable = valami"'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_variable(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._VARIABLE_QUOTE_BEFORE_ERROR == cm.exception.args[0])

    def test__double_check_invalid_variable_1(self):
        line = 'my_variable = valami'
        expected = None
        result = projectfile._invalid_variable(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_variable_2(self):
        line = 'my_variable = "valami"'
        expected = None
        result = projectfile._invalid_variable(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_variable_3(self):
        line = 'my_variable = \'valami\''
        expected = None
        result = projectfile._invalid_variable(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_variable_4(self):
        line = 'my_variable = valami vmi'
        expected = None
        result = projectfile._invalid_variable(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_variable_5(self):
        line = 'my_variable = valami vmi     '
        expected = None
        result = projectfile._invalid_variable(line)
        self.assertEqual(expected, result)


class CommandDivisorParser(TestCase):

    def test__command_divisor_can_be_parsed_1(self):
        line = '==='
        expected = True
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_2(self):
        line = ' ==='
        expected = True
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_3(self):
        line = ' ===      '
        expected = True
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_4(self):
        line = '\t==='
        expected = True
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_5(self):
        line = '=='
        expected = False
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_6(self):
        line = '='
        expected = False
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_7(self):
        line = '= =='
        expected = False
        result = projectfile._command_divisor(line)
        self.assertEqual(expected, result)


class CommandHeaderParser(TestCase):

    def test__valid_command_header__basic_case(self):
        line = 'command:'
        expected = {
            'keywords': ['command'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__command_name_full_range(self):
        line = 'command_COMMAND_1234567890.abc-abc:'
        expected = {
            'keywords': ['command_COMMAND_1234567890.abc-abc'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_after_colon(self):
        line = 'command:   '
        expected = {
            'keywords': ['command'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_before_colon(self):
        line = 'command  :'
        expected = {
            'keywords': ['command'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__two_alternative_commands(self):
        line = 'command|com:'
        expected = {
            'keywords': ['command', 'com'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__three_alternative_commands(self):
        line = 'command|com|c:'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__alternatives_with_space(self):
        line = 'command |  com    | c    :'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': []
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies(self):
        line = 'command|com|c: [dep]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__multiple_dependencies(self):
        line = 'command|com|c: [dep, dep2, dep3]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep', 'dep2', 'dep3']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__full_range_dependencies(self):
        line = 'command|com|c: [command_COMMAND_1234567890.abc-abc]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['command_COMMAND_1234567890.abc-abc']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_no_whitespaces(self):
        line = 'command|com|c:[dep]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_more_outside_whitespaces(self):
        line = 'command|com|c:    [dep]          '
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep    ]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__multiple_dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep  ,               dep1  ]'
        expected = {
            'keywords': ['command', 'com', 'c'],
            'dependencies': ['dep', 'dep1']
        }
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__no_colon(self):
        line = 'command'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__two_colons_1(self):
        line = ':command:'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__two_colons_2(self):
        line = 'command::'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_alternative_list_1(self):
        line = 'command|:'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_alternative_list_2(self):
        line = '|command:'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_dependency_list_1(self):
        line = 'command: [dep'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_dependency_list_2(self):
        line = 'command: dep'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_dependency_list_3(self):
        line = 'command: dep]'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_dependency_list_4(self):
        line = 'command: [dep,]'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__returns_none__wrong_dependency_list_5(self):
        line = 'command: [,,dep]'
        expected = None
        result = projectfile._valid_command_header(line)
        self.assertEqual(expected, result)

    def test__invalid_command_header__raises_exception__indentation_1(self):
        line = ' command'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__indentation_2(self):
        line = '     command'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__indentation_3(self):
        line = '\tcommand'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INDENTATION_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_1(self):
        line = 'command'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_2(self):
        line = 'command|'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__no_colon_3(self):
        line = 'command   [deb]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_MISSING_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_1(self):
        line = 'command:c'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_2(self):
        line = ':command'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_COLON_ERROR == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_1(self):
        line = 'command|:'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_2(self):
        line = '|command:'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_3(self):
        line = '|command|:'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_alternative_list_4(self):
        line = 'command||:'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_ALTERNATIVE == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_1(self):
        line = 'command: []'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_EMPTY_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_2(self):
        line = 'command: ['
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_3(self):
        line = 'command: ]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_4(self):
        line = 'command: [,]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_5(self):
        line = 'command: [ ,]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_6(self):
        line = 'command: [ ,  ]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_7(self):
        line = 'command: [dep1, , dep2]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__invalid_command_header__raises_exception__wrong_dependency_list_8(self):
        line = 'command: [dep1,,dep2]'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_command_header(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue(projectfile._COMMAND_HEADER_INVALID_DEPENDENCY_LIST == cm.exception.args[0])

    def test__double_check_invalid_command_header_1(self):
        line = 'command:'
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_command_header_2(self):
        line = 'command|com:'
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_command_header_3(self):
        line = 'command|com|c:'
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_command_header_4(self):
        line = 'command|com|c: [d1]'
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_command_header_5(self):
        line = 'command|com|c: [d1, d2]'
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)

    def test__double_check_invalid_command_header_6(self):
        line = 'command | com | c  : [ d1        , d2 ]    '
        expected = None
        result = projectfile._invalid_command_header(line)
        self.assertEqual(expected, result)


