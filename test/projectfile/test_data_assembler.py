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

from projects.projectfile import data_processor


class Walker(TestCase):

    @mock.patch.object(data_processor, 'os')
    @mock.patch.object(data_processor, 'parser')
    def test__walker_can_be_mocked_out(self, mock_parser, mock_os):
        mock_os.walk.return_value = [
            ('.', ['A', 'B', 'C'], ['Projectfile']),
            ('./A', [], ['Projectfile']),
            ('./B', ['F'], ['Projectfile']),
            ('./B/F', [], ['Projectfile']),
            ('./C', ['D', 'E'], ['Projectfile']),
            ('./C/D', [], ['Projectfile']),
            ('./C/E', [], ['Projectfile'])
        ]

        for root, dirs, files in mock_os.walk():
            print(root, dirs, files)