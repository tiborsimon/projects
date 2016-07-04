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

import os

from projects import projectfile
from projects.projectfile import error
from projects.projectfile import defs


class ProjectfileModuleFullStackTests(TestCase):
    @mock.patch.object(projectfile.file_handler, 'get_walk_data')
    @mock.patch.object(projectfile.file_handler, '_load')
    def test__root_projectfile_structure_can_be_parsed(self, mock_load, mock_walk):
        dummy_file_contents = [
                '''\
from v1.2.3 #comment
"""
Root level.
"""
a = 42
b = 45

command|com|c:
  """
  Command in root: command
  """
  root pre ${a}
  ===
  root post $b

other_command|oth|oo|o: [command]
  """
  Command in root: other
  """
  root pre 1
  root pre 2
  ===
  root post''',
                '''\
from v2.0.0 #comment
"""
Root/A level.
"""
c = 44
d = 55

command|cc:
  """
  Command in root/A: command
  """
  root/A pre ${c}
  ===
  root/A post $d

other_command|oth|oo|o: [command]
  """
  Command in root/A: other
  """
  root/A pre 1
  root/A pre 2
  ===
  root/A post''',
                '''\
from v2.0.0
"""
Root/A/B level.
"""
command:
    """
  Command in root/A/B: command
  """
  root/A/B pre
  ===
  root/A/B post''',
                '''\
from v2.0.0
"""
Root/C level.
"""
command:
  """
  Command in root/C: command
  """
  root/C pre
  ===
  root/C post'''
        ]
        splitted_content = []
        for file_content in dummy_file_contents:
            splitted_content.append(file_content.split('\n'))
        mock_load.side_effect = splitted_content

        dummy_walk_data = [
            [
                os.path.join('root'),
                ['A', 'C'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A'),
                ['B'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A', 'B'),
                [],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'C'),
                [],
                [defs.PROJECTFILE]
            ]
        ]
        mock_walk.return_value = dummy_walk_data
        expected = {
            'min-version': (1, 2, 3),
            'description': 'Root level.\n\nRoot/A level.\n\nRoot/A/B level.\n\nRoot/C level.',
            'commands': {
                'command': {
                    'alternatives': ['com', 'cc', 'c'],
                    'description': 'Command in root: command\n\nCommand in root/A: command\n\nCommand in root/A/B: command\n\nCommand in root/C: command',
                    'script': [
                        'cd {}'.format(dummy_walk_data[0][0]),
                        'root pre 42',
                        'cd {}'.format(dummy_walk_data[1][0]),
                        'root/A pre 44',
                        'cd {}'.format(dummy_walk_data[2][0]),
                        'root/A/B pre',
                        'root/A/B post',
                        'cd {}'.format(dummy_walk_data[1][0]),
                        'root/A post 55',
                        'cd {}'.format(dummy_walk_data[3][0]),
                        'root/C pre',
                        'root/C post',
                        'cd {}'.format(dummy_walk_data[0][0]),
                        'root post 45'
                    ]
                },
                'com': {
                    'alias': 'command'
                },
                'cc': {
                    'alias': 'command'
                },
                'c': {
                    'alias': 'command'
                },
                'other_command': {
                    'alternatives': ['oth', 'oo', 'o'],
                    'dependencies': ['command'],
                    'description': 'Command in root: other\n\nCommand in root/A: other',
                    'script': [
                        'cd {}'.format(dummy_walk_data[0][0]),
                        'root pre 1',
                        'root pre 2',
                        'cd {}'.format(dummy_walk_data[1][0]),
                        'root/A pre 1',
                        'root/A pre 2',
                        'root/A post',
                        'cd {}'.format(dummy_walk_data[0][0]),
                        'root post'
                    ]
                },
                'oth': {
                    'alias': 'other_command'
                },
                'oo': {
                    'alias': 'other_command'
                },
                'o': {
                    'alias': 'other_command'
                }
            }
        }
        result = projectfile.get_data_for_root('path/root')
        mock_walk.assert_called_with('path/root')
        self.assertEqual(expected, result)


class ErrorCasesAndErrorWrapping(TestCase):
    @mock.patch.object(projectfile.file_handler, 'get_walk_data')
    @mock.patch.object(projectfile.file_handler, '_load')
    def test__syntax_error_in_projectfile__exception_will_wrapped_and_path_will_reported(self, mock_load, mock_walk):
        splitted_content = [
            ['something']
        ]
        mock_load.side_effect = splitted_content

        dummy_walk_data = [
            ('path/root', [], [defs.PROJECTFILE])
        ]
        mock_walk.return_value = dummy_walk_data

        mock_walk.return_value = dummy_walk_data
        with self.assertRaises(Exception) as cm:
            projectfile.get_data_for_root('path/root')
        assert_exception(self, cm, error.ProjectfileError,
                         {
                             'error': error.VERSION_MISSING_ERROR,
                             'line': 1,
                             'path': 'path/root'
                         })


class WalkDataStringforGUI(TestCase):
    @mock.patch.object(projectfile.file_handler, 'get_walk_data')
    @mock.patch.object(projectfile, 'os')
    def test__walk_data_can_be_generated(self, mock_os, mock_walk):
        dummy_walk_data = [
            [
                os.path.join('root'),
                ['A', 'C'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A'),
                ['B'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A', 'B'),
                [],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'C'),
                [],
                [defs.PROJECTFILE]
            ]
        ]
        mock_walk.return_value = dummy_walk_data
        mock_os.path.isfile.return_value = True
        expected = '''\
[x] .
[x] A
[x] A/B
[x] C
'''
        result = projectfile.get_walk_order('root')
        self.assertEqual(expected, result)
        mock_walk.assert_called_with('root')

    @mock.patch.object(projectfile.file_handler, 'get_walk_data')
    @mock.patch.object(projectfile, 'os')
    def test__walk_data_can_be_generated_not_all_directory_contains_projectfile(self, mock_os, mock_walk):
        dummy_walk_data = [
            [
                os.path.join('root'),
                ['A', 'C'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A'),
                ['B'],
                [defs.PROJECTFILE]
            ],
            [
                os.path.join('root', 'A', 'B'),
                [],
                []
            ],
            [
                os.path.join('root', 'C'),
                [],
                [defs.PROJECTFILE]
            ]
        ]
        mock_walk.return_value = dummy_walk_data
        mock_os.path.isfile.side_effect = [True, True, False, True]
        expected = '''\
[x] .
[x] A
[ ] A/B
[x] C
'''
        result = projectfile.get_walk_order('root')
        self.assertEqual(expected, result)
        mock_walk.assert_called_with('root')



