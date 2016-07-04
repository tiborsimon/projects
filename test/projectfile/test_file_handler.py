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
    @mock.patch.object(file_handler, 'parser', autospec=True)
    def test__single_projectfile(self, mock_parser, mock_load, mock_walk):
        dummy_path = 'root'
        dummy_walk = [
            (dummy_path, [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_parsed_data = {
            'dummy': 'parsed',
            'data': 42
        }

        mock_parser.process_lines.return_value = mock_parsed_data
        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            {
                'path': 'root',
                'dummy': 'parsed',
                'data': 42
            }
        ]

        result = file_handler.get_node_list(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        mock_load.assert_called_with(os.path.join(dummy_walk[0][0], dummy_walk[0][2][0]))
        mock_parser.process_lines.assert_called_with(dummy_file_content)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    @mock.patch.object(file_handler, 'parser', autospec=True)
    def test__single_projectfile_with_other_files(self, mock_parser, mock_load, mock_walk):
        dummy_path = 'root'
        dummy_walk = [
            (dummy_path, [], ['other_file_1', 'other_file_2', defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_parsed_data = {
            'dummy': 'parsed',
            'data': 42
        }

        mock_parser.process_lines.return_value = mock_parsed_data
        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            {
                'path': 'root',
                'dummy': 'parsed',
                'data': 42
            }
        ]

        result = file_handler.get_node_list(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        mock_load.assert_called_with(os.path.join(dummy_walk[0][0], dummy_walk[0][2][2]))
        mock_parser.process_lines.assert_called_with(dummy_file_content)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    @mock.patch.object(file_handler, 'parser', autospec=True)
    def test__no_projectfile_on_level__skips_that_level(self, mock_parser, mock_load, mock_walk):
        dummy_path = 'root'
        dummy_walk = [
            (dummy_path, ['A'], [defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'A'), [], ['other'])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_parsed_data = {
            'dummy': 'parsed',
            'data': 42
        }

        mock_parser.process_lines.return_value = mock_parsed_data
        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            {
                'path': 'root',
                'dummy': 'parsed',
                'data': 42
            }
        ]

        result = file_handler.get_node_list(dummy_path)

        mock_walk.assert_called_with(dummy_path)
        mock_parser.process_lines.assert_called_with(dummy_file_content)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    @mock.patch.object(file_handler, 'parser', autospec=True)
    def test__more_complicated_example__full_projectfile_coverage(self, mock_parser, mock_load, mock_walk):
        dummy_path = 'root'
        dummy_walk = [
            (dummy_path, ['A', 'B', 'C'], ['some_file_1', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'A'), [], [defs.PROJECTFILE, 'some_file_1']),
            (os.path.join(dummy_path, 'B'), ['F'], ['some_file_1', 'some_file_2', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'B', 'F'), [], ['some_file_1', 'some_file_1', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'C'), ['D', 'E'], [defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'C', 'D'), [], [defs.PROJECTFILE, 'some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C', 'E'), [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_parsed_data = [
            {
                'dummy-data': 'root'
            },
            {
                'dummy-data': 'root/A'
            },
            {
                'dummy-data': 'root/B'
            },
            {
                'dummy-data': 'root/B/F'
            },
            {
                'dummy-data': 'root/C'
            },
            {
                'dummy-data': 'root/C/D'
            },
            {
                'dummy-data': 'root/C/E'
            }
        ]

        mock_parser.process_lines.side_effect = mock_parsed_data
        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            {
                'path': 'root',
                'dummy-data': 'root'
            },
            {
                'path': 'root/A',
                'dummy-data': 'root/A'
            },
            {
                'path': 'root/B',
                'dummy-data': 'root/B'
            },
            {
                'path': 'root/B/F',
                'dummy-data': 'root/B/F'
            },
            {
                'path': 'root/C',
                'dummy-data': 'root/C'
            },
            {
                'path': 'root/C/D',
                'dummy-data': 'root/C/D'
            },
            {
                'path': 'root/C/E',
                'dummy-data': 'root/C/E'
            }
        ]

        result = file_handler.get_node_list(dummy_path)
        mock_walk.assert_called_with(dummy_path)
        self.assertEqual(expected, result)

    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    @mock.patch.object(file_handler, 'parser', autospec=True)
    def test__more_complicated_example__partial_projectfile_coverage(self, mock_parser, mock_load, mock_walk):
        dummy_path = 'root'
        dummy_walk = [
            (dummy_path, ['A', 'B', 'C'], ['some_file_1']),
            (os.path.join(dummy_path, 'A'), [], ['some_file_1']),
            (os.path.join(dummy_path, 'B'), ['F'], ['some_file_1', 'some_file_2', defs.PROJECTFILE]),
            (os.path.join(dummy_path, 'B', 'F'), [], ['some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C'), ['D', 'E'], []),
            (os.path.join(dummy_path, 'C', 'D'), [], [defs.PROJECTFILE, 'some_file_1', 'some_file_1']),
            (os.path.join(dummy_path, 'C', 'E'), [], [defs.PROJECTFILE])
        ]
        dummy_file_content = ['line 1', 'line 2']

        mock_parsed_data = [
            {
                'dummy-data': 'root/B'
            },
            {
                'dummy-data': 'root/C/D'
            },
            {
                'dummy-data': 'root/C/E'
            }
        ]

        mock_parser.process_lines.side_effect = mock_parsed_data
        mock_walk.return_value = dummy_walk
        mock_load.return_value = dummy_file_content

        expected = [
            {
                'path': 'root/B',
                'dummy-data': 'root/B'
            },
            {
                'path': 'root/C/D',
                'dummy-data': 'root/C/D'
            },
            {
                'path': 'root/C/E',
                'dummy-data': 'root/C/E'
            }
        ]

        result = file_handler.get_node_list(dummy_path)

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
            file_handler.get_node_list(dummy_path)
        assert_exception(self, cm, error.ProjectfileError, {'error': error.PROJECTFILE_NO_PROJECTFILE})


class ExceptionRepacking(TestCase):
    @mock.patch.object(file_handler, 'parser', autospec=True)
    @mock.patch.object(file_handler, 'walk', autospec=True)
    @mock.patch.object(file_handler, '_load', autospec=True)
    def test__exception_occurs__path_gets_added(self, mock_load, mock_walk, mock_parser):
        dummy_path = '.'
        dummy_walk = [
            (dummy_path, [], [defs.PROJECTFILE])
        ]
        mock_walk.return_value = dummy_walk
        mock_parser.process_lines.side_effect = Exception({})

        expected = {
            'path': dummy_path
        }

        with self.assertRaises(Exception) as cm:
            file_handler.get_node_list(dummy_path)
            result = cm.exception.args[0]
            self.assertEqual(expected, result)

