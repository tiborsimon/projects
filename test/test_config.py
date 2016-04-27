#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
try:
    import mock
except ImportError:
    from unittest import mock
import os

from projects import config


class ConfigLoadingTestCases(TestCase):

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    def test__config_path_required_correctly(self, mock_os, mock_json):
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                config.get_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.get_config()
        mock_os.path.expanduser.assert_called_with('~/.prc')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    def test__config_file_is_opened_from_the_right_path(self, mock_os, mock_json):
        dummy_config_path = '/config/path'
        mock_os.path.expanduser.return_value = dummy_config_path
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                config.get_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.get_config()
        mock_open.assert_called_with(dummy_config_path, 'r')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    def test__file_not_found__raises_error(self, mock_os, mock_json):
        mock_open = mock.MagicMock(side_effect = IOError('cannot open file'))
        with self.assertRaises(IOError):
            try:
                with mock.patch('__builtin__.open', mock_open):
                    config.get_config()
            except ImportError:
                with mock.patch('builtins.open', mock_open):
                    config.get_config()

    @mock.patch('projects.config.json')
    def test__parsed_config_file_is_returned(self, mock_json):
        dummy_config = {
            'dummy': 'config'
        }
        mock_json.load.return_value = dummy_config
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                result = config.get_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                result = config.get_config()
        self.assertEqual(dummy_config, result)

    @mock.patch('projects.config.json')
    def test__invalid_json_syntax__raises_error(self, mock_json):
        mock_json.load.side_effect = SyntaxError('json invalid')
        mock_open = mock.MagicMock()
        with self.assertRaises(SyntaxError):
            try:
                with mock.patch('__builtin__.open', mock_open):
                    config.get_config()
            except ImportError:
                with mock.patch('builtins.open', mock_open):
                    config.get_config()


class ConfigValidationtEstCases(TestCase):

    def test__mandatory_keys_present__no_exception_raised(self):
        pass
