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
                config.load_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.load_config()
        mock_os.path.expanduser.assert_called_with('~/.prc')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    def test__config_file_is_opened_from_the_right_path(self, mock_os, mock_json):
        dummy_config_path = '/config/path'
        mock_os.path.expanduser.return_value = dummy_config_path
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                config.load_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.load_config()
        mock_open.assert_called_with(dummy_config_path, 'r')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    def test__file_not_found__raises_error(self, mock_os, mock_json):
        mock_open = mock.MagicMock(side_effect = IOError('cannot open file'))
        with self.assertRaises(IOError):
            try:
                with mock.patch('__builtin__.open', mock_open):
                    config.load_config()
            except ImportError:
                with mock.patch('builtins.open', mock_open):
                    config.load_config()

    @mock.patch('projects.config.json')
    def test__parsed_config_file_is_returned(self, mock_json):
        dummy_config = {
            'dummy': 'config'
        }
        mock_json.load.return_value = dummy_config
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                result = config.load_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                result = config.load_config()
        self.assertEqual(dummy_config, result)

    @mock.patch('projects.config.json')
    def test__invalid_json_syntax__raises_error(self, mock_json):
        mock_json.load.side_effect = SyntaxError('json invalid')
        mock_open = mock.MagicMock()
        with self.assertRaises(SyntaxError):
            try:
                with mock.patch('__builtin__.open', mock_open):
                    config.load_config()
            except ImportError:
                with mock.patch('builtins.open', mock_open):
                    config.load_config()


class ConfigValidationTestCases(TestCase):

    def test__mandatory_keys_present__no_exception_raised(self):
        dc = config.default_config
        config.validate(dc, dc)

    def test__missing_keys__raises_appropriate_exception(self):
        dc = config.default_config

        with self.assertRaises(KeyError):
            dummy_config = {
                'selection-mode-index-not-fuzzy': False
            }
            config.validate(dummy_config, dc)

    def test__invalid_key__raises_exception(self):
        dc = config.default_config
        invalid_config = {
            'projects-path': '~/projects',
            'selection-mode-index-not-fuzzy': True,
            'asdfasdfasdfasdf': 'asdf'
        }

        with self.assertRaises(SyntaxError):
            config.validate(invalid_config, dc)


class ConfigCreationTestCases(TestCase):

    @mock.patch('projects.config.os')
    @mock.patch('projects.config.json')
    def test__write_path_calculated_correctly(self, mock_json, mock_os):
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                config.create_default_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.create_default_config()
        mock_os.path.expanduser.assert_called_with('~/.prc')


    @mock.patch('projects.config.os')
    @mock.patch('projects.config.json')
    def test__config_is_written_to_the_right_place(self, mock_json,  mock_os):
        dummy_path = '/project/path'
        mock_os.path.expanduser.return_value = dummy_path
        mock_open = mock.MagicMock()
        try:
            with mock.patch('__builtin__.open', mock_open):
                config.create_default_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open):
                config.create_default_config()
        mock_open.assert_called_with(dummy_path, 'w+')

    @mock.patch('projects.config.os')
    @mock.patch('projects.config.json')
    def test__json_is_written_with_the_default_config(self, mock_json,  mock_os):
        df = config.default_config
        mock_open = mock.mock_open()
        try:
            with mock.patch('__builtin__.open', mock_open, create=True):
                config.create_default_config()
        except ImportError:
            with mock.patch('builtins.open', mock_open, create=True):
                config.create_default_config()
        mock_json.dump.assert_called_with(mock_open.return_value, df)


class ConfigInitializationTestCases(TestCase):

    @mock.patch('projects.config.load_config')
    def test__loaded_config_saved_as_a_global_variable(self, mock_load):
        dummy_config = {'my_dict': 123}
        mock_load.return_value = dummy_config
        self.assertEqual({}, config.current_config)
        config.init()
        self.assertEqual(dummy_config, config.current_config)

    @mock.patch('projects.config.load_config')
    @mock.patch('projects.config.create_default_config')
    def test__config_file_not_exits__creates_new_one(self, mock_create, mock_load):
        mock_load.side_effect = IOError()
        mock_load.return_value = {}
        config.init()
        mock_create.assert_called()











