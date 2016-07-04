#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects.projectfile import error
from projects.projectfile.parser import parse
from test.helpers import *


class VersionParser(TestCase):
    def test__valid_version_can_be_parsed_1(self):
        line = 'from v1.2.3'
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_2(self):
        line = 'from 1.2.3'
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_3(self):
        line = 'from           v1.2.3    '
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__valid_version_can_be_parsed_4(self):
        line = 'from v123456789.23456789.3456789'
        expected = (123456789, 23456789, 3456789)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_1(self):
        line = 'from v1.2.3 #comment'
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_2(self):
        line = 'from v1.2.3 # comment'
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_3(self):
        line = 'from v1.2.3#comment'
        expected = (1, 2, 3)
        result = parse.version(line)
        self.assertEqual(expected, result)

    def test__invalid_version__raise_exception_1(self):
        line = ' from v1.2.3'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_INDENTATION_ERROR)

    def test__invalid_version__raise_exception_2(self):
        line = '       from v1.2.3'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_INDENTATION_ERROR)

    def test__invalid_version__raise_exception_3(self):
        line = '\t\tfrom v1.2.3'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_INDENTATION_ERROR)

    def test__invalid_version__raise_exception_4(self):
        line = 'from v1.2'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)

    def test__invalid_version__raise_exception_5(self):
        line = 'from v1.2_4'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)

    def test__invalid_version__raise_exception_6(self):
        line = 'from #v1.2.4'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)

    def test__invalid_version__raise_exception_7(self):
        line = 'from v#1.2.4'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)

    def test__invalid_version__raise_exception_8(self):
        line = 'from v1.2#.4'
        with self.assertRaises(Exception) as cm:
            parse.version(line)
        assert_exception(self, cm, SyntaxError, error.VERSION_FORMAT_ERROR)

    def test__not_version_related_input__returns_none(self):
        line = 'something'
        expected = None
        result = parse.version(line)
        self.assertEqual(expected, result)


class EmptyLineParser(TestCase):
    def test__parse_empty_line_1(self):
        line = ''
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_2(self):
        line = ' '
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_3(self):
        line = '\t'
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_4(self):
        line = 'valami'
        expected = False
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__parse_empty_line_5(self):
        line = '  valami'
        expected = False
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_1(self):
        line = '#comment'
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_2(self):
        line = '    #comment'
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_3(self):
        line = '    #    comment'
        expected = True
        result = parse.empty_line(line)
        self.assertEqual(expected, result)


class IndentedLineParser(TestCase):
    def test__parse_indented_line_1(self):
        line = ' valami'
        expected = 'valami'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_2(self):
        line = '           valami'
        expected = 'valami'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_3(self):
        line = ' valami valamik    '
        expected = 'valami valamik'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__parse_indented_line_4(self):
        line = 'valami'
        expected = None
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_1(self):
        line = ' valami#comment'
        expected = 'valami'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_2(self):
        line = ' valami  #comment'
        expected = 'valami'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_3(self):
        line = ' valami  #      comment'
        expected = 'valami'
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__cant_tolerate_only_comment_1(self):
        line = ' #comment'
        expected = None
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__cant_tolerate_only_comment_2(self):
        line = '   #   comment'
        expected = None
        result = parse.indented_line(line)
        self.assertEqual(expected, result)

    def test__cant_tolerate_only_comment_3(self):
        line = '#comment'
        expected = None
        result = parse.indented_line(line)
        self.assertEqual(expected, result)


class CommentDelimiterParser(TestCase):
    def test__delimiter_can_be_parsed__zero_indentation(self):
        line = '"""'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__delimiter_can_be_parsed__one_indentation(self):
        line = ' """'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__delimiter_can_be_parsed__one_indentation_with_tab(self):
        line = '\t"""'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__delimiter_can_be_parsed__two_indentations(self):
        line = '  """'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__delimiter_can_be_parsed__two_indentations__tailing_indentations_ignored(self):
        line = '  """                    \t\t\t   '
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__invalid_delimiter_returns_false_1(self):
        line = '""'
        expected = False
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__invalid_delimiter_returns_false_2(self):
        line = '" ""'
        expected = False
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__invalid_delimiter_returns_false_3(self):
        line = '"""something'
        expected = False
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_1(self):
        line = '"""#coment'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_2(self):
        line = '"""  #coment'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_3(self):
        line = '"""  #      coment'
        expected = True
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)

    def test__cant_tolerate_comment(self):
        line = '#"""'
        expected = False
        result = parse.comment_delimiter(line)
        self.assertEqual(expected, result)


class LineParser(TestCase):
    def test__line_can_be_parsed_1(self):
        line = 'valami'
        expected = 'valami'
        result = parse.line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_2(self):
        line = ' valami'
        expected = 'valami'
        result = parse.line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_3(self):
        line = '   valami    '
        expected = 'valami'
        result = parse.line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_4(self):
        line = '\t\tvalami    '
        expected = 'valami'
        result = parse.line(line)
        self.assertEqual(expected, result)

    def test__line_can_be_parsed_5(self):
        line = ' valami valami    '
        expected = 'valami valami'
        result = parse.line(line)
        self.assertEqual(expected, result)

    def test__comment_will_be_collected_as_well(self):
        line = 'valami #comment'
        expected = 'valami #comment'
        result = parse.line(line)
        self.assertEqual(expected, result)


class VariableParser(TestCase):
    def test__variable_can_be_parsed__basic_case(self):
        line = 'my_variable = valami'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__more_whitespaces(self):
        line = 'my_variable   =   valami'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__no_whitespace(self):
        line = 'my_variable=valami'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__full_range_variable_name(self):
        line = '1234567890.abc-abc = valami'
        expected = {'1234567890.abc-abc': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value(self):
        line = 'my_variable = valami vmi'
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__whitespace_inside_value_and_after_value(self):
        line = 'my_variable = valami vmi     '
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value(self):
        line = 'my_variable = "valami vmi"'
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_tailing_whitespace(self):
        line = 'my_variable = "valami vmi"     '
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = "valami\\"vmi"'
        expected = {'my_variable': 'valami"vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__double_quoted_value_with_escaped_quote(self):
        line = 'my_variable = "valami\\\'vmi"'
        expected = {'my_variable': 'valami\'vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value(self):
        line = 'my_variable = \'valami vmi\''
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_tailing_whitespace(self):
        line = 'my_variable = \'valami vmi\'     '
        expected = {'my_variable': 'valami vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_double_quote(self):
        line = 'my_variable = \'valami\\"vmi\''
        expected = {'my_variable': 'valami"vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__variable_can_be_parsed__quoted_value_with_escaped_quote(self):
        line = 'my_variable = \'valami\\\'vmi\''
        expected = {'my_variable': 'valami\'vmi'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_1(self):
        line = 'my_variable = valami#comment'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_2(self):
        line = 'my_variable = valami   #comment'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__can_tolerate_comment_3(self):
        line = 'my_variable = valami   #    comment'
        expected = {'my_variable': 'valami'}
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__completely_wrong_syntax_returns_none_1(self):
        line = 'something'
        expected = None
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__completely_wrong_syntax_returns_none_2(self):
        line = 'something # = variable'
        expected = None
        result = parse.variable(line)
        self.assertEqual(expected, result)

    def test__invalid_variable__indentation_should_raise_exception__basic_case(self):
        line = ' my_variable = valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_INDENTATION_ERROR)

    def test__invalid_variable__indentation_should_raise_exception__more_whitespaces(self):
        line = '         my_variable = valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_INDENTATION_ERROR)

    def test__invalid_variable__indentation_should_raise_exception__tabs(self):
        line = '\t\tmy_variable = valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_INDENTATION_ERROR)

    def test__invalid_full_range_variable__indentation_should_raise_exception(self):
        line = ' 1234567890.abc-abc = valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_INDENTATION_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_quote_1(self):
        line = 'my_variable = \'valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_AFTER_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_quote_2(self):
        line = 'my_variable = valami\''
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_BEFORE_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_quote_3(self):
        line = 'my_variable = \'valami#\''
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_AFTER_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_double_quote_1(self):
        line = 'my_variable = "valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_AFTER_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_double_quote_2(self):
        line = 'my_variable = valami"'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_BEFORE_ERROR)

    def test__invalid_variable__should_raise_exception__unmatched_double_quote_3(self):
        line = 'my_variable = "valami#"'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_QUOTE_AFTER_ERROR)

    def test__invalid_variable__should_raise_exception__commented_out_value_1(self):
        line = 'my_variable = #valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_SYNTAX_ERROR)

    def test__invalid_variable__should_raise_exception__commented_out_value_2(self):
        line = 'my_variable =#valami'
        with self.assertRaises(Exception) as cm:
            parse.variable(line)
        assert_exception(self, cm, SyntaxError, error.VARIABLE_SYNTAX_ERROR)


class CommandDivisorParser(TestCase):
    def test__command_divisor_can_be_parsed_1(self):
        line = '==='
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_2(self):
        line = ' ==='
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_3(self):
        line = ' ===      '
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_4(self):
        line = '\t==='
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_5(self):
        line = '=='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_6(self):
        line = '='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_7(self):
        line = '= =='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_8(self):
        line = '===valami'
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_be_parsed_9(self):
        line = '=== valami'
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_tolerate_comment_1(self):
        line = '===#comment'
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_tolerate_comment_2(self):
        line = '===  #comment'
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__command_divisor_can_tolerate_comment_3(self):
        line = '===  #   comment'
        expected = True
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__commented_out_divisor__returns_false_1(self):
        line = '#==='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__commented_out_divisor__returns_false_2(self):
        line = '#  ==='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)

    def test__commented_out_divisor__returns_false_3(self):
        line = '  #  ==='
        expected = False
        result = parse.command_divisor(line)
        self.assertEqual(expected, result)


class CommandHeaderParser(TestCase):
    def test__valid_command_header__basic_case(self):
        line = 'command:'
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__command_name_full_range(self):
        line = 'command_COMMAND_1234567890.abc-abc:'
        expected = {
            'command_COMMAND_1234567890.abc-abc': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_after_colon(self):
        line = 'command:   '
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__extra_space_before_colon(self):
        line = 'command  :'
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__two_alternative_commands(self):
        line = 'command|com:'
        expected = {
            'command': {
                'alternatives': ['com'],
                'done': False
            },
            'com': {
                'alias': 'command'
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__three_alternative_commands(self):
        line = 'command|com|c:'
        expected = {
            'command': {
                'alternatives': ['com', 'c'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__alternatives_with_space(self):
        line = 'command |  com    | c    :'
        expected = {
            'command': {
                'alternatives': ['com', 'c'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__alternatives_are_sorted_in_decending_length_order(self):
        line = 'command|c|com:'
        expected = {
            'command': {
                'alternatives': ['com', 'c'],
                'done': False
            },
            'com': {
                'alias': 'command'
            },
            'c': {
                'alias': 'command'
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__dependencies(self):
        line = 'command|com|c: [dep]'
        expected = ['dep']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__multiple_dependencies(self):
        line = 'command|com|c: [dep, dep2, dep3]'
        expected = ['dep', 'dep2', 'dep3']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__full_range_dependencies(self):
        line = 'command|com|c: [command_COMMAND_1234567890.abc-abc]'
        expected = ['command_COMMAND_1234567890.abc-abc']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__dependencies_with_no_whitespaces(self):
        line = 'command|com|c:[dep]'
        expected = ['dep']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__dependencies_with_more_outside_whitespaces(self):
        line = 'command|com|c:    [dep]          '
        expected = ['dep']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep    ]'
        expected = ['dep']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__multiple_dependencies_with_more_inside_whitespaces(self):
        line = 'command|com|c: [ dep  ,               dep1  ]'
        expected = ['dep', 'dep1']
        result = parse.command_header(line)
        self.assertEqual(expected, result['command']['dependencies'])

    def test__valid_command_header__can_tolerate_comment_1(self):
        line = 'command:#comment'
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__can_tolerate_comment_2(self):
        line = 'command:    #comment'
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__can_tolerate_comment_3(self):
        line = 'command:    #     comment'
        expected = {
            'command': {
                'done': False
            }
        }
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__valid_command_header__can_tolerate_comment_4(self):
        line = 'command|com|c:[dep,dep1]#comment'
        expected = {
            'command': {
                'alternatives': ['com', 'c'],
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
        result = parse.command_header(line)
        self.assertEqual(expected, result)

    def test__invalid_command_header__raises_exception__indentation_1(self):
        line = ' command:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INDENTATION_ERROR)

    def test__invalid_command_header__raises_exception__indentation_2(self):
        line = '     command:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INDENTATION_ERROR)

    def test__invalid_command_header__raises_exception__indentation_3(self):
        line = '\tcommand:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INDENTATION_ERROR)

    def test__invalid_command_header__raises_exception__indentation_4(self):
        line = ' command'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)

    def test__invalid_command_header__raises_exception__no_colon_1(self):
        line = 'command'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__invalid_command_header__raises_exception__no_colon_2(self):
        line = 'command|'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__invalid_command_header__raises_exception__no_colon_3(self):
        line = 'command   [deb]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_1(self):
        line = 'command:c'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_COLON_ERROR)

    def test__invalid_command_header__raises_exception__wrong_colon_syntax_2(self):
        line = ':command'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_COLON_ERROR)

    def test__invalid_command_header__raises_exception__wrong_alternative_list_1(self):
        line = 'command|:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_ALTERNATIVE)

    def test__invalid_command_header__raises_exception__wrong_alternative_list_2(self):
        line = '|command:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_ALTERNATIVE)

    def test__invalid_command_header__raises_exception__wrong_alternative_list_3(self):
        line = '|command|:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_ALTERNATIVE)

    def test__invalid_command_header__raises_exception__wrong_alternative_list_4(self):
        line = 'command||:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_ALTERNATIVE)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_1(self):
        line = 'command: []'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_EMPTY_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_2(self):
        line = 'command: ['
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_3(self):
        line = 'command: [valami'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_4(self):
        line = 'command: ]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_5(self):
        line = 'command: [,]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_6(self):
        line = 'command: [ ,]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_7(self):
        line = 'command: [ ,  ]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_8(self):
        line = 'command: [dep1, , dep2]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__wrong_dependency_list_9(self):
        line = 'command: [dep1,,dep2]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST)

    def test__invalid_command_header__raises_exception__comment_in_definition_1(self):
        line = 'command#:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__invalid_command_header__raises_exception__comment_in_definition_2(self):
        line = '#command:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_MISSING_COLON_ERROR)

    def test__invalid_command_header__raises_exception__comment_in_dependency_list_1(self):
        line = 'command: [dep1,#dep2]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)

    def test__invalid_command_header__raises_exception__comment_in_dependency_list_2(self):
        line = 'command: [dep1,  #dep2]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)

    def test__invalid_command_header__raises_exception__comment_in_dependency_list_3(self):
        line = 'command: [dep1,  #           dep2]'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_SYNTAX_ERROR)

    def test__prohibited_command_name__raises_error(self):
        line = 'p:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_PROHIBITED_COMMAND.format('p'))

    def test__prohibited_alternative_name__raises_error(self):
        line = 'pommand|p:'
        with self.assertRaises(Exception) as cm:
            parse.command_header(line)
        assert_exception(self, cm, SyntaxError, error.COMMAND_HEADER_PROHIBITED_COMMAND.format('p'))