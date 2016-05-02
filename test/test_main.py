#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    from unittest import mock

try:
    import __builtin__
    open_mock_string = '__builtin__.open'
except ImportError:
    open_mock_string = 'builtins.open'

from projects import p
from projects import config


class Config(TestCase):

    @mock.patch.object(p, 'config', autospec=True)
    @mock.patch.object(p, 'paths', autospec=True)
    def test__config_loaded_and_used_correctly(self, mock_path, mock_config):
        mock_path.inside_project.return_value = True
        mock_config.get.return_value = config._default_config
        p.main(())
        mock_path.inside_project.assert_called_with(config._default_config['projects-path'])
        # TODO: mock out further calls
