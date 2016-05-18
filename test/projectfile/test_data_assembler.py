#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import os

try:
    import mock
except ImportError:
    from unittest import mock

try:
    import __builtin__
    builtin_module = '__builtin__'
except ImportError:
    builtin_module = 'builtins'

from projects.projectfile import data_processor
from projects.projectfile import file_handler


class ProcessingTreeCreation(TestCase):

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_single_file(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = ['line 1', 'line 2']
        dummy_walk = [
            (project_root, dummy_file_content)
        ]
        dummy_data = {'dummy_data': True}

        mock_file_handler.projectfile_walk.return_value = dummy_walk
        mock_parser.process_lines.return_value = dummy_data

        expected = {
            'path': project_root,
            'data': dummy_data,
            'children': []
        }

        result = data_processor.generate_processing_tree(project_root)

        mock_parser.process_lines.assert_called_with(dummy_file_content)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_one_deep_structure(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = ['line 1', 'line 2']
        dummy_walk = [
            (project_root, dummy_file_content),
            (os.path.join(project_root, 'A'), dummy_file_content)
        ]
        dummy_data = {'dummy_data': True}

        mock_file_handler.projectfile_walk.return_value = dummy_walk
        mock_parser.process_lines.return_value = dummy_data

        expected = {
            'path': project_root,
            'data': dummy_data,
            'children': [{
                'path': dummy_walk[1][0],
                'data': dummy_data,
                'children': []
            }]
        }

        result = data_processor.generate_processing_tree(project_root)

        mock_parser.process_lines.assert_called_with(dummy_file_content)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)


#     @mock.patch.object(data_processor, 'os')
#     @mock.patch.object(data_processor, 'parser')
#     def test__temp(self, mock_parser, mock_os):
#         mock_os.walk.return_value = [
#             ('.', ['A', 'B', 'C'], ['Projectfile']),
#             ('./A', [], ['Projectfile']),
#             ('./B', ['F'], ['Projectfile']),
#             ('./B/F', [], ['Projectfile']),
#             ('./C', ['D', 'E'], ['Projectfile']),
#             ('./C/D', [], ['Projectfile']),
#             ('./C/E', [], ['Projectfile'])
#         ]