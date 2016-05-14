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

from projects.projectfile import file_handler


class FileLoading(TestCase):
    def test__load_method_called_with_the_right_path(self):
        dummy_path = '/dummy/path'
        with mock.patch(builtin_module + '.open') as mock_open:
            file_handler._load(dummy_path)
            mock_open.assert_called_with(dummy_path, 'r')

    def test__load_method_returns_the_loaded_file_content_as_a_list_of_string(self):
        mock_open = mock.mock_open(read_data='line 1\nline 2')
        expected = ['line 1', 'line 2']
        with mock.patch(builtin_module + '.open', mock_open):
            result = file_handler._load('...')
            self.assertEqual(expected, result)