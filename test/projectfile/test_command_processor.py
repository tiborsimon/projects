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

from projects.projectfile import command_processor
from projects.projectfile import error


class GeneratingCommandTree(TestCase):
    def test__only_pre(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A']
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__only_pre__in_two_parallel_folders_with_same_command__should_append_them(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre B']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A']
                        },
                        {
                            'path': 'B',
                            'pre': ['pre B']
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__post_with_no_child(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__post_with_child(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__same_commands_with_children_and_parallel(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            },
            {
                'path': 'C',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre C'],
                        'post': ['post C']
                    }
                }
            },
            {
                'path': 'C/D',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre D'],
                        'post': ['post D']
                    }
                }
            },
            {
                'path': 'C/D/E',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'pre': ['pre E'],
                        'post': ['post E']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        },
                        {
                            'path': 'C',
                            'pre': ['pre C'],
                            'post': ['post C'],
                            'children': [
                                {
                                    'path': 'C/D',
                                    'pre': ['pre D'],
                                    'post': ['post D'],
                                    'children': [
                                        {
                                            'path': 'C/D/E',
                                            'pre': ['pre E'],
                                            'post': ['post E']
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__child_with_different_command(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command-parent': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command-child': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command-parent': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                },
                'my-command-child': {
                    'root': [
                        {
                            'path': 'B',
                            'pre': ['pre B'],
                            'post': ['post B']
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__child_with_alternative_only_naming(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'c': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['c'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                },
                'c': {
                    'alias': 'command'
                }

            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__child_with_different_and_common_commands(self):
        processing_tree = [
            {
                'path': 'A',
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
                }
            },
            {
                'path': 'A/B',
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
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command-A': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                },
                'command-B': {
                    'root': [
                        {
                            'path': 'A/B',
                            'pre': ['pre B'],
                            'post': ['post B']
                        }
                    ]
                },
                'command-common': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre common A'],
                            'post': ['post common A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre common B'],
                                    'post': ['post common B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__root_with_two_children(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            },
            {
                'path': 'A/C',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'pre': ['pre C'],
                        'post': ['post C']
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                },
                                {
                                    'path': 'A/C',
                                    'pre': ['pre C'],
                                    'post': ['post C']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)


class AlternativeHandling(TestCase):
    def test__single_file_single_command__alternative_presents(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['c'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                },
                'c': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__alternative_presents_in_child(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['c'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                },
                'c': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__two_alternatives_in_two_master_and_childl(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['ca'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'ca': {
                        'alias': 'command'
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['cb'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'cb': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['ca', 'cb'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                },
                'ca': {
                    'alias': 'command'
                },
                'cb': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__two_alternatives_in_two_separate_nodes(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['ca'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'ca': {
                        'alias': 'command'
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['cb'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'cb': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['ca', 'cb'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        },
                        {
                            'path': 'B',
                            'pre': ['pre B'],
                            'post': ['post B']
                        }
                    ]
                },
                'ca': {
                    'alias': 'command'
                },
                'cb': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__alternative_redefined_for_the_same_command_in_separate_node__should_be_tolerated(self):
        self.maxDiff = None
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives': ['c'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        },
                        {
                            'path': 'B',
                            'pre': ['pre B'],
                            'post': ['post B']
                        }
                    ]
                },
                'c': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__alternative_redefined_for_the_same_command_in_child__should_be_tolerated(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'alternatives': ['c'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'c': {
                        'alias': 'command'
                    }
                }
            }
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'alternatives' : ['c'],
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                },
                'c': {
                    'alias': 'command'
                }
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result)

    def test__two_commands_with_same_alternative_in_child__raises_error(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command1': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command1'
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command2': {
                        'alternatives': ['c'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'c': {
                        'alias': 'command2'
                    }
                }
            }
        ]
        with self.assertRaises(Exception) as cm:
            command_processor.generate_command_tree(processing_tree)
        self.assertEqual(cm.exception.__class__, error.ProjectfileError)

    def test__two_commands_with_same_alternative_in_separate_node__raises_error(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command1': {
                        'alternatives': ['c'],
                        'pre': ['pre A'],
                        'post': ['post A']
                    },
                    'c': {
                        'alias': 'command1'
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command2': {
                        'alternatives': ['c'],
                        'pre': ['pre B'],
                        'post': ['post B']
                    },
                    'c': {
                        'alias': 'command2'
                    }
                }
            }
        ]
        with self.assertRaises(Exception) as cm:
            command_processor.generate_command_tree(processing_tree)
        self.assertEqual(cm.exception.__class__, error.ProjectfileError)


class FinalizingDescriptions(TestCase):
    def test__description_handling__main_description_will_be_added(self):
        processing_tree = [
            {
                'path': 'my_path',
                'min-version': (1, 2, 3),
                'description': 'Some text..',
                'commands': {
                    'my-command': {
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                }
            }
        ]
        expected = 'Some text..'
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['description'])

    def test__more_than_one_main_description__will_be_appended__separate_nodes(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'description': 'Some text..',
                'commands': {
                    'command_A': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'description': 'Another main description..',
                'commands': {
                    'command_B': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = 'Some text..\n\nAnother main description..'
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['description'])

    def test__more_than_one_main_description__will_be_appended__child(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'description': 'Root',
                'commands': {
                    'command_A': {
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'description': 'Child',
                'commands': {
                    'command_B': {
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = 'Root\n\nChild'
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['description'])

    def test__command_description_will_be_added(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'my-command': {
                        'description': 'Some text..',
                        'pre': ['echo "pre"'],
                        'post': ['echo "post"']
                    }
                }
            }
        ]
        expected = 'Some text..'
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['my-command']['description'])

    def test__redefined_command_description_will_be_appended(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Another main description..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = 'Some text..\n\nAnother main description..'
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['command']['description'])


class FinalizeVersions(TestCase):
    def test__single_version_finalizes_correctly(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            }
        ]
        expected = (1, 2, 3)
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_parallel_versions__smallest_should_be_kept(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = (1, 2, 3)
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_parallel_versions__smallest_should_be_kept__even_in_reverse_order(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = (1, 2, 3)
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['min-version'])

    def test__redefined_version_works_with_child_nodes_as_well(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (2, 0, 0),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre A'],
                        'post': ['post A']
                    }
                }
            },
            {
                'path': 'A/B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command': {
                        'description': 'Some text..',
                        'pre': ['pre B'],
                        'post': ['post B']
                    }
                }
            }
        ]
        expected = (1, 2, 3)
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['min-version'])


class AppendVariables(TestCase):
    def test__variables_appended_in_parallel_arrangement(self):
        processing_tree = [
            {
                'path': 'A',
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
                }
            },
            {
                'path': 'B',
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
                }
            }
        ]
        expected = {
            'variable-a': {
                'value': 'aaa',
                'path': 'A'
            },
            'variable-b': {
                'value': 'bbb',
                'path': 'B'
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['variables'])

    def test__variables_appended_in_child_arrangement(self):
        processing_tree = [
            {
                'path': 'A',
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
                }
            },
            {
                'path': 'A/B',
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
                }
            }
        ]
        expected = {
            'variable-a': {
                'value': 'aaa',
                'path': 'A'
            },
            'variable-b': {
                'value': 'bbb',
                'path': 'A/B'
            }
        }
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['variables'])

    def test__redefined_variable__raises_error(self):
        processing_tree = [
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
                }
            },
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
                }
            }
        ]
        with self.assertRaises(Exception) as cm:
            command_processor.generate_command_tree(processing_tree)
        assert_exception(self, cm, error.ProjectfileError, {
            'error': error.VARIABLE_REDEFINED_ERROR.format('variable-a', 'path_A', 'path_B'),
            'path': 'path_B'
        })


class DependencyAddition(TestCase):
    def test__dependencies_can_be_added(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'pre': ['pre B']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_B': {
                        'dependencies': ['command_A'],
                        'pre': ['pre B']
                    }
                }
            }
        ]
        expected = ['command_A']
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['command_B']['dependencies'])

    def test__dependencies_get_appended_if_not_already_in_the_list(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'dependencies': ['command_B', 'command_C'],
                        'pre': ['pre B']
                    },
                    'command_B': {
                        'pre': ['pre B']
                    },
                    'command_C': {
                        'pre': ['pre C']
                    },
                    'command_D': {
                        'pre': ['pre D']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'dependencies': ['command_B', 'command_D'],
                        'pre': ['pre A']
                    },
                    'command_B': {
                        'pre': ['pre B']
                    },
                    'command_D': {
                        'pre': ['pre D']
                    }
                }
            }
        ]
        expected = ['command_B', 'command_C', 'command_D']
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['command_A']['dependencies'])


class AlternativesAddition(TestCase):
    def test__alternatives_can_be_added(self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'alternatives': ['com', 'c'],
                        'pre': ['pre B']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_B': {
                        'dependencies': 'command_A',
                        'pre': ['pre B']
                    }
                }
            }
        ]
        expected = ['com', 'c']
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['command_A']['alternatives'])

    def test__alternatives_in_multiple_levels_can_be_added   (self):
        processing_tree = [
            {
                'path': 'A',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'alternatives': ['com', 'c'],
                        'pre': ['pre B']
                    }
                }
            },
            {
                'path': 'B',
                'min-version': (1, 2, 3),
                'commands': {
                    'command_A': {
                        'alternatives': ['cc'],
                        'pre': ['pre B']
                    }
                }
            }
        ]
        expected = ['com', 'cc', 'c']
        result = command_processor.generate_command_tree(processing_tree)
        self.assertEqual(expected, result['commands']['command_A']['alternatives'])

class FlatteningCommands(TestCase):
    def test__simple_command_with_pre_and_post_with_no_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'post A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__alias_can_be_tolerated(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        }
                    ]
                },
                'a': {
                    'alias': 'my-command'
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'post A'
                    ]
                },
                'a': {
                    'alias': 'my-command'
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_only_pre(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_only_post(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'post': ['post A']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'post A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_pre_and_post_with_one_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd A/B',
                        'pre B',
                        'post B',
                        'cd A',
                        'post A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_only_pre_with_one_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd A/B',
                        'pre B',
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_only_post_with_one_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A/B',
                        'post B',
                        'cd A',
                        'post A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_no_post_with_one_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd A/B',
                        'post B'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__simple_command_with_one_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd A/B',
                        'pre B',
                        'post B',
                        'cd A',
                        'post A'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__parallel_commands_pre_only_with_no_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A']
                        },
                        {
                            'path': 'B',
                            'pre': ['pre B']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd B',
                        'pre B'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__parallel_commands_post_only_with_no_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'post': ['post A']
                        },
                        {
                            'path': 'B',
                            'post': ['post B']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'post A',
                        'cd B',
                        'post B'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__parallel_commands_with_no_child(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A']
                        },
                        {
                            'path': 'B',
                            'pre': ['pre B'],
                            'post': ['post B']
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'post A',
                        'cd B',
                        'pre B',
                        'post B'
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)

    def test__parallel_commands_with_children(self):
        command_tree = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'root': [
                        {
                            'path': 'A',
                            'pre': ['pre A'],
                            'post': ['post A'],
                            'children': [
                                {
                                    'path': 'A/B',
                                    'pre': ['pre B'],
                                    'post': ['post B']
                                }
                            ]
                        },
                        {
                            'path': 'C',
                            'pre': ['pre C'],
                            'post': ['post C'],
                            'children': [
                                {
                                    'path': 'C/D',
                                    'pre': ['pre D'],
                                    'post': ['post D']
                                }
                            ]
                        }
                    ]
                }
            }
        }
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'my-command': {
                    'script': [
                        'cd A',
                        'pre A',
                        'cd A/B',
                        'pre B',
                        'post B',
                        'cd A',
                        'post A',
                        'cd C',
                        'pre C',
                        'cd C/D',
                        'pre D',
                        'post D',
                        'cd C',
                        'post C',
                    ]
                }
            }
        }
        command_processor.flatten_commands(command_tree)
        self.assertEqual(expected, command_tree)


class VariableSubstitution(TestCase):
    def test__substitution_function_recognize_variable_with_short_syntax(self):
        line = '$magic'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '42'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

    def test__substitution_function_recognize_variable_with_long_syntax(self):
        line = '${magic}'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '42'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

    def test__substitution_function_recognize_variable_with_short_syntax__in_text(self):
        line = '...$magic...'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '...42...'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

    def test__substitution_function_recognize_variable_with_long_syntax__in_text(self):
        line = '...${magic}...'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '...42...'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

    def test__missing_escapement__no_substitution(self):
        line = '...{magic}...'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '...{magic}...'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

    def test__missing_escapement__no_substitution_case_2(self):
        line = '...magic...'
        variables = {
            'magic': {
                'value': '42'
            }
        }
        expected = '...magic...'
        result = command_processor.substitute_variables(line, variables)
        self.assertEqual(expected, result)

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
                        'cd $var_a'
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
        command_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_commands(self):
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
                        'cd ${var_a}',
                        'echo ${var_b}'
                    ]
                },
                'other_command': {
                    'script': [
                        'cd $var_b',
                        'echo $var_a'
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
        command_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_main_description(self):
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
            'description': '$var_a ... $var_b',
            'commands': {
                'command': {
                    'script': [
                        'cd $var_a',
                        'echo $var_b'
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
        command_processor.process_variables(data)
        self.assertEqual(expected, data)

    def test__multiple_variables_can_be_substituted_to_command_descriptions(self):
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
                    'description': '$var_a ... $var_b',
                    'script': [
                        'cd $var_a',
                        'echo $var_b'
                    ]
                },
                'other_command': {
                    'description': '$var_b ... $var_a',
                    'script': [
                        'cd $var_b',
                        'echo $var_a'
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
        command_processor.process_variables(data)
        self.assertEqual(expected, data)


