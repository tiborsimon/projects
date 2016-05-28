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

from projects import projectfile
from projects.projectfile import error
from projects.projectfile import data_processor


class ProjectfileModuleFullStackTests(TestCase):
    @mock.patch.object(projectfile.data_processor.file_handler, 'projectfile_walk')
    def test__single_root_projectfile_can_be_parsed(self, mock_walk):
        self.maxDiff = None
        dummy_walk_data = [
            (
                'path/root',
                [
                    'from v1.2.3',
                    '"""',
                    'This is a test..',
                    '"""',
                    'a = 42',
                    'b = 45',
                    '',
                    'command|com|c:',
                    '  """',
                    '  This is the command description.',
                    '  vmi',
                    '  """',
                    '  echo "pre"',
                    '  ===',
                    '  echo "post"',
                    '',
                    'other_command|oth|oo|o: [command]',
                    '  """',
                    '  Another command..',
                    '  """',
                    '  echo "other"',
                    '  echo "something"',
                    '  ===',
                    '  echo "post2"'
                ]
            )
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is a test..',
            'commands': {
                'command': {
                    'description': 'This is the command description. vmi',
                    'script' :[
                        'cd path/root',
                        'echo "pre"',
                        'echo "post"'
                    ]
                },
                'com': {
                    'alias': 'command'
                },
                'c': {
                    'alias': 'command'
                },
                'other_command': {
                    'dependencies': ['command'],
                    'description': 'Another command..',
                    'script': [
                        'cd path/root',
                        'echo "other"',
                        'echo "something"',
                        'echo "post2"'
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
        mock_walk.return_value = dummy_walk_data
        data = projectfile.get_data_for_root('path/root')
        mock_walk.assert_called_with('path/root')
        self.assertEqual(expected, data)

