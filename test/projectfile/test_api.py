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
    def test__single_root_projectfile_can_be_parsed(self, mock_file_handler):
        mock_file_handler.return_value = ()
        projectfile.get_data_for_root('.')
        mock_file_handler.assert_called_with('.')
