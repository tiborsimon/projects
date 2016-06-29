#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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

from projects.projectfile import file_handler
from projects.projectfile import error
from projects.projectfile import defs
from test.helpers import *


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


class ProjectfileWalk(TestCase):
    @mock.patch.object(file_handler, 'get_walk_data', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__single_projectfile(self, mock_load, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            (dummy_path, [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            ('.', dummy_file_content)
        ]

        result = file_handler.projectfile_walk(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        mock_load.assert_called_with(os.path.join(dummy_walk[0][0], dummy_walk[0][2][0]))
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__single_projectfile_with_other_files(self, mock_load, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            (dummy_path, [], ['other_file_1', 'other_file_2', defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            ('.', dummy_file_content)
        ]

        result = file_handler.projectfile_walk(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        mock_load.assert_called_with(os.path.join(dummy_walk[0][0], dummy_walk[0][2][2]))
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__no_projectfile_on_level__skips_that_level(self, mock_load, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            (dummy_path, ['A'], [defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'A'), [], ['other'])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            ('.', dummy_file_content)
        ]

        result = file_handler.projectfile_walk(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__more_complicated_example__full_projectfile_coverage(self, mock_load, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            ('.', ['A', 'B', 'C'], ['some_file_1', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'A'), [], [defs.PROJECTFILE, 'some_file_1']),
            (os.path.join(dummy_path, 'B'), ['F'], ['some_file_1', 'some_file_2', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'B', 'F'), [], ['some_file_1', 'some_file_1', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'C'), ['D', 'E'], [defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'C', 'D'), [], [defs.PROJECTFILE, 'some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C', 'E'), [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            ('.', dummy_file_content),
            (os.path.join(dummy_path, 'A'), dummy_file_content),
            (os.path.join(dummy_path, 'B'), dummy_file_content),
            (os.path.join(dummy_path, 'B', 'F'), dummy_file_content),
            (os.path.join(dummy_path, 'C'), dummy_file_content),
            (os.path.join(dummy_path, 'C', 'D'), dummy_file_content),
            (os.path.join(dummy_path, 'C', 'E'), dummy_file_content)
        ]

        result = file_handler.projectfile_walk(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__more_complicated_example__partial_projectfile_coverage(self, mock_load, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            ('.', ['A', 'B', 'C'], ['some_file_1']),
            (os.path.join(dummy_path, 'A'), [], ['some_file_1']),
            (os.path.join(dummy_path, 'B'), ['F'], ['some_file_1', 'some_file_2', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'B', 'F'), [], ['some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C'), ['D', 'E'], []),
            (os.path.join(dummy_path, 'C', 'D'), [], [defs.PROJECTFILE, 'some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C', 'E'), [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            (os.path.join(dummy_path, 'B'), dummy_file_content),
            (os.path.join(dummy_path, 'C', 'D'), dummy_file_content),
            (os.path.join(dummy_path, 'C', 'E'), dummy_file_content)
        ]

        result = file_handler.projectfile_walk(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        self.assertEqual(expected, result)


class ErrorHandling(TestCase):
    @mock.patch.object(file_handler, 'walk', autospec=True)
    def test__no_projectfile_at_all__raises_error(self, mock_walk):
        dummy_path = '.'
        dummy_walk = [
            (dummy_path, [], [])
        ]

        mock_walk.return_value = dummy_walk

        with self.assertRaises(Exception) as cm:
            file_handler.projectfile_walk(dummy_path)
        assert_exception(self, cm, error.ProjectfileError, {'error': error.PROJECTFILE_NO_PROJECTFILE})


