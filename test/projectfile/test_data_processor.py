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

from test.helpers import *

from projects.projectfile import data_processor
from projects.projectfile import error


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


class FinalizingCommands(TestCase):
    def test__only_pre(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A']
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
                        'cd path_A',
                        'pre A'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__only_pre__in_two_parallel_folders_with_same_command__should_append_them(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre B']
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
                        'cd path_A',
                        'pre A',
                        'cd path_B',
                        'pre B'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__post_with_no_child(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
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
                        'cd path_A',
                        'pre A',
                        'post A'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__post_with_child(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'my-command': {
                                'pre': ['pre B'],
                                'post': ['post B']
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
                        'cd path_A',
                        'pre A',
                        'cd path_B',
                        'pre B',
                        'post B',
                        'post A'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__same_commands_with_children_and_parallel(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'my-command': {
                                'pre': ['pre B'],
                                'post': ['post B']
                            }
                        },
                        'children': []
                    }
                ]
            },
            {
                'path': 'path_C',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre C'],
                        'post': ['post C']
                    }
                },
                'children': [
                    {
                        'path': 'path_D',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'my-command': {
                                'pre': ['pre D'],
                                'post': ['post D']
                            }
                        },
                        'children': [
                            {
                                'path': 'path_E',
                                'min-version': (1, 2, 3),
                                'commands': {
                                    'my-command': {
                                        'pre': ['pre E'],
                                        'post': ['post E']
                                    }
                                },
                                'children': []
                            }
                        ]
                    }
                ]
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd path_A',
                        'pre A',
                        'cd path_B',
                        'pre B',
                        'post B',
                        'post A',
                        'cd path_C',
                        'pre C',
                        'cd path_D',
                        'pre D',
                        'cd path_E',
                        'pre E',
                        'post E',
                        'post D',
                        'post C'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__child_with_different_command(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command-parent': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'my-command-child': {
                                'pre': ['pre B'],
                                'post': ['post B']
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
                'my-command-parent': {
                    'script': [
                        'cd path_A',
                        'pre A',
                        'post A'
                    ]
                },
                'my-command-child': {
                    'script': [
                        'cd path_B',
                        'pre B',
                        'post B',
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)

    def test__child_with_different_and_common_commands(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command-A': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'command-common': {
                        'pre': ['pre common A'],
                        'post': ['post common A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'command-B': {
                                'pre': ['pre B'],
                                'post': ['post B']
                            },
                            'command-common': {
                                'pre': ['pre common B'],
                                'post': ['post common B']
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
                'command-A': {
                    'script': [
                        'cd path_A',
                        'pre A',
                        'post A'
                    ]
                },
                'command-B': {
                    'script': [
                        'cd path_B',
                        'pre B',
                        'post B'
                    ]
                },
                'command-common': {
                    'script': [
                        'cd path_A',
                        'pre common A',
                        'cd path_B',
                        'pre common B',
                        'post common B',
                        'post common A'
                    ]
                }
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result)


class FinalizingDescriptions(TestCase):
    def test__description_handling__main_description_will_be_added(self):
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
        expected = 'Some text..'
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['description'])

    def test__more_than_one_main_description__will_be_appended(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'description': 'Some text..',
                'commands': {
                    'command_A': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (1, 2, 3),
                'description': 'Another main description..',
                'commands': {
                    'command_B': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                },
                'children': []
            }
        ]
        expected = 'Some text..\n\nAnother main description..'
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['description'])

    def test__command_description_will_be_added(self):
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
        expected = 'Some text..'
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['commands']['my-command']['description'])

    def test__redefined_command_description_will_be_appended(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Another main description..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                },
                'children': []
            }
        ]
        expected = 'Some text..\n\nAnother main description..'
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['commands']['command']['description'])


class FinalizeVersions(TestCase):
    def test__single_version_finalizes_correctly(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            }
        ]
        expected = (1, 2, 3)
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_parallel_versions__latest_should_be_kept(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                },
                'children': []
            }
        ]
        expected = (2, 0, 0)
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_parallel_versions__latest_should_be_kept__even_in_reverse_order(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                },
                'children': []
            }
        ]
        expected = (2, 0, 0)
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_version_works_with_child_nodes_as_well(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'commands': {
                            'command': {
                                'description': 'Some text..',
                                'pre': ['pre B'],
                                'post': ['post B']
                            }
                        },
                        'children': []
                    }
                ]
            }
        ]
        expected = (2, 0, 0)
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['min-version'])


class AppendVariables(TestCase):
    def test__variables_appended_in_parallel_arrangement(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (2, 0, 0),
                'variables': {
                    'variable-a': 'aaa'
                },
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': []
            },
            {
                'path': 'path_B',
                'min-version': (1, 2, 3),
                'variables': {
                    'variable-b': 'bbb'
                },
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                },
                'children': []
            }
        ]
        expected = {
            'variable-a': {
                'value': 'aaa',
                'path': 'path_A'
            },
            'variable-b': {
                'value': 'bbb',
                'path': 'path_B'
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['variables'])

    def test__variables_appended_in_child_arrangement(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (2, 0, 0),
                'variables': {
                    'variable-a': 'aaa'
                },
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'variables': {
                            'variable-b': 'bbb'
                        },
                        'commands': {
                            'command': {
                                'description': 'Some text..',
                                'pre': ['pre B'],
                                'post': ['post B']
                            }
                        },
                        'children': []
                    }
                ]
            }
        ]
        expected = {
            'variable-a': {
                'value': 'aaa',
                'path': 'path_A'
            },
            'variable-b': {
                'value': 'bbb',
                'path': 'path_B'
            }
        }
        result = data_processor.finalize_data(input_data)
        self.assertEqual(expected, result['variables'])

    def test__redefined_variable__raises_error(self):
        input_data = [
            {
                'path': 'path_A',
                'min-version': (2, 0, 0),
                'variables': {
                    'variable-a': 'aaa'
                },
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                },
                'children': [
                    {
                        'path': 'path_B',
                        'min-version': (1, 2, 3),
                        'variables': {
                            'variable-a': 'bbb'
                        },
                        'commands': {
                            'command': {
                                'description': 'Some text..',
                                'pre': ['pre B'],
                                'post': ['post B']
                            }
                        },
                        'children': []
                    }
                ]
            }
        ]
        with self.assertRaises(Exception) as cm:
            result = data_processor.finalize_data(input_data)
        assert_exception(self, cm, error.ProjectfileError, {
            'error': error.VARIABLE_REDEFINED_ERROR.format('variable-a', 'path_B', 'path_A'),
            'path': 'path_A'
        })


class VariableSubstitution(TestCase):
    def test__variable_can_be_substituted_to_commands(self):
        data = {
            'variables': {
                'var_a': {
                    'value': 'aaa'
                }
            },
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'script': [
                        'cd var_a'
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'script': [
                        'cd aaa'
                    ]
                }
            }
        }
        result = data_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_commands(self):
        self.maxDiff = None
        data = {
            'variables': {
                'var_a': {
                    'value': 'aaa'
                },
                'var_b': {
                    'value': 'bbb'
                }
            },
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'script': [
                        'cd var_a',
                        'echo var_b'
                    ]
                },
                'other_command': {
                    'script': [
                        'cd var_b',
                        'echo var_a'
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'script': [
                        'cd aaa',
                        'echo bbb'
                    ]
                },
                'other_command': {
                    'script': [
                        'cd bbb',
                        'echo aaa'
                    ]
                }
            }
        }
        result = data_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_main_description(self):
        self.maxDiff = None
        data = {
            'variables': {
                'var_a': {
                    'value': 'aaa'
                },
                'var_b': {
                    'value': 'bbb'
                }
            },
            'min-version': (1, 2, 3),
            'description': 'var_a ... var_b',
            'commands': {
                'command': {
                    'script': [
                        'cd var_a',
                        'echo var_b'
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'description': 'aaa ... bbb',
            'commands': {
                'command': {
                    'script': [
                        'cd aaa',
                        'echo bbb'
                    ]
                }
            }
        }
        result = data_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_command_descriptions(self):
        self.maxDiff = None
        data = {
            'variables': {
                'var_a': {
                    'value': 'aaa'
                },
                'var_b': {
                    'value': 'bbb'
                }
            },
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'var_a ... var_b',
                    'script': [
                        'cd var_a',
                        'echo var_b'
                    ]
                },
                'other_command': {
                    'description': 'var_b ... var_a',
                    'script': [
                        'cd var_b',
                        'echo var_a'
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'aaa ... bbb',
                    'script': [
                        'cd aaa',
                        'echo bbb'
                    ]
                },
                'other_command': {
                    'description': 'bbb ... aaa',
                    'script': [
                        'cd bbb',
                        'echo aaa'
                    ]
                }
            }
        }
        result = data_processor.process_variables(data)
        self.assertEqual(expected, data)



