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


def update_expected_with_parsed_data(update_data, expected):
    def update_node(update_data, node, index):
        node.update(update_data[index])
        index += 1
        for child in node['children']:
            index = update_node(update_data, child, index)
        return index

    index = 0
    for node in expected:
        index = update_node(update_data, node, index)




class HelperFunctions(TestCase):
    def test__processing_tree_result__case_1(self):
        input_data = [
            {'dummy_data': True}
        ]
        data = [
            {
                'children': []
            }
        ]
        expected = [
            {
                'children': [],
                'dummy_data': True
            }
        ]
        update_expected_with_parsed_data(input_data, data)
        self.assertEqual(expected, data)

    def test__processing_tree_result__case_2(self):
        input_data = [
            {'dummy_data_0': True},
            {'dummy_data_1': True}
        ]
        data = [
            {
                'children': []
            },
            {
                'children': []
            }
        ]
        expected = [
            {
                'children': [],
                'dummy_data_0': True
            },
            {
                'children': [],
                'dummy_data_1': True
            }
        ]
        update_expected_with_parsed_data(input_data, data)
        self.assertEqual(expected, data)

    def test__processing_tree_result__case_3(self):
        input_data = [
            {'dummy_data_0': True},
            {'dummy_data_1': True}
        ]
        data = [
            {
                'children': [
                    {
                        'children': []
                    }
                ]
            }
        ]
        expected = [
            {
                'dummy_data_0': True,
                'children': [
                    {
                        'dummy_data_1': True,
                        'children': []
                    }
                ],

            }
        ]
        update_expected_with_parsed_data(input_data, data)
        self.assertEqual(expected, data)

    def test__processing_tree_result__case_4(self):
        input_data = [
            {'dummy_data_0': True},
            {'dummy_data_1': True},
            {'dummy_data_2': True},
            {'dummy_data_3': True}
        ]
        data = [
            {
                'children': [
                    {
                        'children': [
                            {
                                'children': []
                            }
                        ]
                    }
                ]
            },
            {
                'children': []
            }
        ]
        expected = [
            {
                'dummy_data_0': True,
                'children': [
                    {
                        'dummy_data_1': True,
                        'children': [
                            {
                                'dummy_data_2': True,
                                'children': []
                            }
                        ]
                    }
                ]
            },
            {
                'dummy_data_3': True,
                'children': []
            }
        ]
        update_expected_with_parsed_data(input_data, data)
        self.assertEqual(expected, data)

    def test__processing_tree_result__case_4(self):
        input_data = [
            {'dummy_data_0': True},
            {'dummy_data_1': True},
            {'dummy_data_2': True},
            {'dummy_data_3': True}
        ]
        data = [
            {
                'children': []
            },
            {
                'children': [
                    {
                        'children': [
                            {
                                'children': []
                            }
                        ]
                    }
                ]
            }
        ]
        expected = [
            {
                'dummy_data_0': True,
                'children': []
            },
            {
                'dummy_data_1': True,
                'children': [
                    {
                        'dummy_data_2': True,
                        'children': [
                            {
                                'dummy_data_3': True,
                                'children': []
                            }
                        ]
                    }
                ]
            }
        ]
        update_expected_with_parsed_data(input_data, data)
        self.assertEqual(expected, data)


class ProcessingTreeCreation(TestCase):
    @mock.patch.object(data_processor, 'file_handler', autospec=True)
    @mock.patch.object(data_processor, 'parser', autospec=True)
    def test__processing_tree_can_be_created_for_single_root_file(self, mock_parser, mock_file_handler):
        project_root = '.'
        dummy_file_content = ['line 1', 'line 2']
        dummy_walk_result = [
            (project_root, dummy_file_content)
        ]
        dummy_parsed_data = [{'dummy_data': True}]

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.side_effect = dummy_parsed_data

        expected = [
            {
                'path': project_root,
                'children': []
            }
        ]
        update_expected_with_parsed_data(dummy_parsed_data, expected)

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
        dummy_parsed_data = [{'dummy_data': True}]

        mock_file_handler.projectfile_walk.return_value = dummy_walk_result
        mock_parser.process_lines.side_effect = dummy_parsed_data

        expected = [
            {
                'path': dummy_walk_result[0][0],
                'children': []
            }
        ]
        update_expected_with_parsed_data(dummy_parsed_data, expected)

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
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'children': []
                    }
                ]
            }
        ]
        update_expected_with_parsed_data(dummy_parsed_data, expected)

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
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'children': [
                            {
                                'path': dummy_walk_result[2][0],
                                'children': []
                            }
                        ]
                    },
                    {
                        'path': dummy_walk_result[3][0],
                        'children': []
                    }
                ]
            }
        ]
        update_expected_with_parsed_data(dummy_parsed_data, expected)

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
                'children': [
                    {
                        'path': dummy_walk_result[1][0],
                        'children': []
                    }
                ]
            },
            {
                'path': dummy_walk_result[2][0],
                'children': []
            }
        ]
        update_expected_with_parsed_data(dummy_parsed_data, expected)

        result = data_processor.generate_processing_tree(project_root)

        process_lines_calls = [
            mock.call(dummy_file_content[0]),
            mock.call(dummy_file_content[1]),
            mock.call(dummy_file_content[2])
        ]
        mock_parser.process_lines.assert_has_calls(process_lines_calls)
        mock_file_handler.projectfile_walk.assert_called_with(project_root)
        self.assertEqual(expected, result)


class DataFinalizer(TestCase):
    def test__only_pre(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path',
                        'echo "pre"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__only_pre__in_two_parallel_folders_with_same_command__should_append_them(self):
        input_data = [
            {
                'path': 'my_path_0',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre 0"']
                    }
                },
                'children': []
            },
            {
                'path': 'my_path_1',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre 1"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path_0',
                        'echo "pre 0"',
                        'cd my_path_1',
                        'echo "pre 1"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__post_with_no_child(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path',
                        'echo "pre"',
                        'echo "post"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__post_with_child(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                },
                'children': [
                    {
                        'path': 'my_path_child',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'my-command': {
                                'pre': ['echo "pre child"'],
                                'post': ['echo "post child"']
                            }
                        },
                        'children': []
                    }
                ]
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path',
                        'echo "pre"',
                        'cd my_path_child',
                        'echo "pre child"',
                        'echo "post child"',
                        'echo "post"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__description_handling__main_description(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'description': 'Some text..',
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'Some text..',
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path',
                        'echo "pre"',
                        'echo "post"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__more_than_one_main_description__will_be_appended(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'description': 'Some text..',
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'Some text..',
            'commands': {
                'my-command': {
                    'script': [
                        'cd my_path',
                        'echo "pre"',
                        'echo "post"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__description_handling__command_description(self):
        input_data = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'description': 'Some text..',
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'description': 'Some text..',
                    'script': [
                        'cd my_path',
                        'echo "pre"',
                        'echo "post"'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)
