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


class ProcessingTreeCreation(TestCase):

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_single_root_file(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = ['line 1', 'line 2']
        dummy_walk_result = [
            (project_root, dummy_file_content)
        ]
        dummy_parsed_data = {'dummy_data': True}

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.return_value = dummy_parsed_data

        expected = [
            {
                'path': project_root,
                'data': dummy_parsed_data,
                'children': []
            }
        ]

        result = data_processor.generate_processing_tree(project_root)

        mock_parser.process_lines.assert_called_with(dummy_file_content)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_single_non_root_file(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = ['line 1', 'line 2']
        dummy_walk_result = [
            (os.path.join(project_root, 'A', 'B', 'C', 'D'), dummy_file_content)
        ]
        dummy_parsed_data = {'dummy_data': True}

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.return_value = dummy_parsed_data

        expected = [
            {
                'path': dummy_walk_result[0][0],
                'data': dummy_parsed_data,
                'children': []
            }
        ]

        result = data_processor.generate_processing_tree(project_root)

        mock_parser.process_lines.assert_called_with(dummy_file_content)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_one_deep_structure(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = [
            ['content root'],
            ['content A']
        ]
        dummy_walk_result = [
            (project_root, dummy_file_content[0]),
            (os.path.join(project_root, 'A'), dummy_file_content[1])
        ]
        dummy_parsed_data = [
            {'dummy_data_root': True},
            {'dummy_data_A': True}
        ]

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.side_effect = dummy_parsed_data

        expected = [
            {
                'path': dummy_walk_result[0][0],
                'data': dummy_parsed_data[0],
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'data': dummy_parsed_data[1],
                        'children': []
                    }
                ]
            }
        ]

        result = data_processor.generate_processing_tree(project_root)

        process_lines_calls = [
            mock.call(dummy_file_content[0]),
            mock.call(dummy_file_content[1])
        ]
        mock_parser.process_lines.assert_has_calls(process_lines_calls)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_one_deep_structure_2(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = [
            ['content root'],
            ['content A'],
            ['content AB'],
            ['content C']
        ]
        dummy_walk_result = [
            (project_root, dummy_file_content[0]),
            (os.path.join(project_root, 'A'), dummy_file_content[1]),
            (os.path.join(project_root, 'A', 'B'), dummy_file_content[2]),
            (os.path.join(project_root, 'C'), dummy_file_content[3])
        ]
        dummy_parsed_data = [
            {'dummy_data_root': True},
            {'dummy_data_A': True},
            {'dummy_data_AB': True},
            {'dummy_data_C': True}
        ]

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.side_effect = dummy_parsed_data

        expected = [
            {
                'path': project_root,
                'data': dummy_parsed_data[0],
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'data': dummy_parsed_data[1],
                        'children': [
                            {
                                'path': dummy_walk_result[2][0],
                                'data': dummy_parsed_data[2],
                                'children': []
                            }
                        ]
                    },
                    {
                        'path': dummy_walk_result[3][0],
                        'data': dummy_parsed_data[3],
                        'children': []
                    }
                ]
            }
        ]

        result = data_processor.generate_processing_tree(project_root)

        process_lines_calls = [
            mock.call(dummy_file_content[0]),
            mock.call(dummy_file_content[1]),
            mock.call(dummy_file_content[2]),
            mock.call(dummy_file_content[3])
        ]
        mock_parser.process_lines.assert_has_calls(process_lines_calls)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)

    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_no_root_projectfile(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = [
            ['content A'],
            ['content AB'],
            ['content C']
        ]
        dummy_walk_result = [
            (os.path.join(project_root, 'A'), dummy_file_content[0]),
            (os.path.join(project_root, 'A', 'B'), dummy_file_content[1]),
            (os.path.join(project_root, 'C'), dummy_file_content[2])
        ]
        dummy_parsed_data = [
            {'dummy_data_A': True},
            {'dummy_data_AB': True},
            {'dummy_data_C': True}
        ]

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.side_effect = dummy_parsed_data

        expected = [
            {
                'path': dummy_walk_result[0][0],
                'data': dummy_parsed_data[0],
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'data': dummy_parsed_data[1],
                        'children': []
                    }
                ]
            },
            {
                'path': dummy_walk_result[2][0],
                'data': dummy_parsed_data[2],
                'children': []
            }
        ]

        result = data_processor.generate_processing_tree(project_root)

        process_lines_calls = [
            mock.call(dummy_file_content[0]),
            mock.call(dummy_file_content[1]),
            mock.call(dummy_file_content[2])
        ]
        mock_parser.process_lines.assert_has_calls(process_lines_calls)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)
