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
        self.assertTrue('Whitespaces are not allowed before the "from" keyword!' == cm.exception.args[0])

    def test__invalid_version__raise_exception_2(self):
        line = 'from v1.2'
        with self.assertRaises(Exception) as cm:
            projectfile._invalid_version(line)
        self.assertEqual(cm.exception.__class__, SyntaxError)
        self.assertTrue('Invalid version format. The valid one looks like "v1.2.3".' == cm.exception.args[0])

    def test__double_check_invalid_version_with_valid_string(self):
        line = 'from v1.2.3'
        expected = None
        result = projectfile._invalid_version(line)
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