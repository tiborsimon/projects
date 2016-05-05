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
