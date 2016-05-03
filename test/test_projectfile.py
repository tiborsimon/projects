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


class VersionParsing(TestCase):

    def test__mandatory_version_can_be_parsed_1(self):
        raw_file = ['from v1.2.3', '']
        expected = {
            'min-version': (1, 2, 3)
        }
        result = projectfile._parse(raw_file)
        self.assertEqual(expected, result)

    def test__mandatory_version_can_be_parsed_2(self):
        raw_file = ['from 1.2.3', '']
        expected = {
            'min-version': (1, 2, 3)
        }
        result = projectfile._parse(raw_file)
        self.assertEqual(expected, result)

    def test__mandatory_version_can_be_parsed_3(self):
        raw_file = ['from           v1.2.3    ', '']
        expected = {
            'min-version': (1, 2, 3)
        }
        result = projectfile._parse(raw_file)
        self.assertEqual(expected, result)

    def test__mandatory_version_can_be_parsed_4(self):
        raw_file = ['', 'from v1.2.3', '']
        expected = {
            'min-version': (1, 2, 3)
        }
        result = projectfile._parse(raw_file)
        self.assertEqual(expected, result)

    def test__invalid_mandatory_version__raise_exception(self):
        raw_file = [' from v1.2.3', '']
        with self.assertRaises(Exception) as cm:
            projectfile._parse(raw_file)
        self.assertEqual(cm.exception.__class__, projectfile.ProjectfileError)
        self.assertTrue('Syntax error in line 1: '
                        'Whitespaces are not allowed before the "from" keyword!' == cm.exception.args[0])

    def test__invalid_mandatory_version__raise_exception_2(self):
        raw_file = ['', ' from v1.2.3', '']
        with self.assertRaises(Exception) as cm:
            projectfile._parse(raw_file)
        self.assertEqual(cm.exception.__class__, projectfile.ProjectfileError)
        self.assertTrue('Syntax error in line 2: '
                        'Whitespaces are not allowed before the "from" keyword!' == cm.exception.args[0])

    def test__mandatory_version_missing__raise_exception(self):
        raw_file = ['', '']
        with self.assertRaises(Exception) as cm:
            projectfile._parse(raw_file)
        self.assertEqual(cm.exception.__class__, projectfile.ProjectfileError)
        self.assertTrue('Syntax error: Mandatory minimum version (from vx.x.x) is missing! '
                        'That should be the first thing you define in your Projectfile.' == cm.exception.args[0])