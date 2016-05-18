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


# class ProcessingTreeCreation(TestCase):
#
#     @mock.patch.object(data_processor, 'os', autospec=True)
#     @mock.patch.object(data_processor, 'file_handler', autospec=True)
#     @mock.patch.object(data_processor, 'parser', autospec=True)
#     def test__processing_tree_can_be_created_for_single_file(self, mock_parser, mock_file_handler, mock_os):
#         dummy_walk =  [
#             ('.', [], ['Projectfile'])
#         ]
#         dummy_file_content = ['line 1', 'line 2']
#         dummy_data = {'dummy_data': True}
#
#
#         mock_os.walk.return_value = dummy_walk
#         mock_file_handler.get_file_content.return_value = ['line 1', 'line 2']
#         mock_parser.process_lines.return_value = dummy_data
#
#         expected = {
#             'path': '.',
#             'data': dummy_data,
#             'children': []
#         }
#
#         result = data_processor.generate_processing_tree()
#
#         mock_file_handler.assert_called_with(os.path.join(dummy_walk[0][0], dummy_walk[0][2][0]))
#         self.assertEqual(expected, result)
#
#
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