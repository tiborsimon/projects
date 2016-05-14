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

from projects.projectfile import error
from projects.projectfile import data_processor


class DataIntegrityTest(TestCase):
    def test__dependecies_refers_to_existing_commands__raises_no_error(self):
        data = {
            'commands': {
                'c1': {},
                'c2': {
                    'dependencies': ['c1']
                }
            }
        }
        data_processor.data_integrity_check(data)

    def test__non_existing_dependency__raises_error(self):
        data = {
            'commands': {
                'c1': {},
                'c2': {
                    'dependencies': ['c']
                }
            }
        }
        with self.assertRaises(Exception) as cm:
            data_processor.data_integrity_check(data)
        assert_exception(self, cm, error.ProjectfileError,
                         {'error': error.PROJECTFILE_INVALID_DEPENDENCY.format('c', 'c2')})