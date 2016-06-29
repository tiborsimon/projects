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

from test.helpers import *

from projects import config


class Path(TestCase):

    @mock.patch.object(config, 'os', autospec=True)
    def test__path_expanded_correctly(self, mock_os):
        config._get_config_path()
        mock_os.path.expanduser.assert_called_with('~/.prc')


class Loading(TestCase):

    @mock.patch.object(config, 'yaml', autospec=True)
    @mock.patch.object(config, 'os', autospec=True)
    def test__config_path_required_correctly(self, mock_os, mock_yaml):
        with mock.patch(open_mock_string):
            config._load_config()
        mock_os.path.expanduser.assert_called_with(config._CONFIG_FILE)

    @mock.patch.object(config, 'yaml', autospec=True)
    @mock.patch.object(config, '_get_config_path', autospec=True)
    def test__config_file_is_opened_from_the_right_path(self, mock_path, mock_yaml):
        dummy_config_path = '/config/path'
        mock_path.return_value = dummy_config_path
        with mock.patch(open_mock_string) as mock_open:
            config._load_config()
            mock_open.assert_called_with(dummy_config_path, 'r')

    @mock.patch.object(config, 'yaml', autospec=True)
    def test__file_not_found__raises_error(self, mock_yaml):
        error_message = 'file not found'
        mock_open = mock.MagicMock(side_effect = IOError(error_message))
        with self.assertRaises(Exception) as cm:
            with mock.patch(open_mock_string, mock_open):
                config._load_config()
        assert_exception(self, cm, IOError, error_message)

    @mock.patch.object(config, 'yaml', autospec=True)
    def test__parsed_config_file_is_returned(self, mock_yaml):
        dummy_config = {'dummy': 'config'}
        mock_yaml.safe_load.return_value = dummy_config
        with mock.patch(open_mock_string):
            result = config._load_config()
        self.assertEqual(dummy_config, result)

    @mock.patch.object(config, 'yaml', autospec=True)
    def test__invalid_yaml_syntax__raises_error(self, mock_yaml):
        error_message = 'yaml invalid'
        mock_yaml.safe_load.side_effect = SyntaxError(error_message)
        with self.assertRaises(Exception) as cm:
            with mock.patch(open_mock_string):
                config._load_config()
        assert_exception(self, cm, SyntaxError, error_message)


class Validation(TestCase):

    def test__mandatory_keys_present__no_exception_raised(self):
        dc = config._default_config
        config._validate(dc)

    def test__missing_mandatory_key__raises_key_error(self):
        with self.assertRaises(Exception) as cm:
            dummy_config = {}
            config._validate(dummy_config)
        assert_exception_type(self, cm, KeyError)

    def test__invalid_mandatory_key__raises_syntax_error(self):
        invalid_config = {
            'projects-path': '~/projects',
            'invalid_key': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        assert_exception_type(self, cm, SyntaxError)

    def test__invalid_optional_key__raises_syntax_error(self):
        invalid_config = {
            'projects-path': '~/projects',
            'invalid-key': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        assert_exception_type(self, cm, SyntaxError)

    def test__invalid_mandatory_value__raises_value_error(self):
        invalid_config = {
            'projects-path': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        assert_exception_type(self, cm, ValueError)

    def test__invalid_optional_value__raises_value_error(self):
        invalid_config = {
            'projects-path': '~/projects',
            'number-color': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        assert_exception_type(self, cm, SyntaxError)


class Creation(TestCase):

    @mock.patch.object(config, '_get_config_path', autospec=True)
    @mock.patch.object(config, 'yaml', autospec=True)
    def test__config_is_written_to_the_right_place(self, mock_yaml, mock_path):
        dummy_path = '/config/path'
        mock_path.return_value = dummy_path
        with mock.patch(open_mock_string) as mock_open:
            config._create_default_config()
            mock_open.assert_called_with(dummy_path, 'w+')

    @mock.patch.object(config, '_get_config_path', autospec=True)
    @mock.patch.object(config, 'yaml', autospec=True)
    def test__file_cannot_be_written__raises_error(self, mock_yaml, mock_path):
        with mock.patch(open_mock_string) as mock_open:
            mock_open.side_effect = IOError()
            with self.assertRaises(Exception) as cm:
                config._create_default_config()
            assert_exception_type(self, cm, IOError)

    @mock.patch.object(config, 'yaml', autospec=True)
    def test__yaml_file_is_written_with_the_full_configuration(self, mock_yaml):
        mock_open = mock.mock_open()
        with mock.patch(open_mock_string, mock_open):
            config._create_default_config()
        mock_yaml.dump.assert_called_with(config._default_config, mock_open.return_value, default_flow_style=False)


class Getter(TestCase):
    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, 'os', autospec=True)
    def test__loaded_projects_path_expanded(self, mock_os, mock_load):
        dummy_config = dict(config._default_config)
        mock_load.return_value = dummy_config
        config.get()
        mock_os.path.expanduser.assert_called_with(dict(config._default_config)['projects-path'])

    @mock.patch.object(config, '_load_config', autospec=True)
    def test__loaded_config_returned(self, mock_load):
        dummy_config = dict(config._default_config)
        mock_load.return_value = dummy_config
        result = config.get()
        self.assertEqual(dummy_config, result)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_create_default_config', autospec=True)
    def test__config_file_not_exits__creates_new_one(self, mock_create, mock_load):
        mock_load.side_effect = [IOError(), dict(config._default_config)]
        config.get()
        mock_create.assert_called_with()

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_create_default_config', autospec=True)
    def test__config_file_cannot_be_written__raises_config_error(self, mock_create, mock_load):
        mock_load.side_effect = IOError()
        error_message = 'Some error..'
        mock_create.side_effect = IOError(error_message)
        with self.assertRaises(Exception) as cm:
            config.get()
        assert_exception(self, cm, config.ConfigError, config._FILE_CREATION_ERROR.format(error_message))

    @mock.patch.object(config, '_load_config', autospec=True)
    def test__invalid_yaml_syntax__raises_config_error(self, mock_load):
        error_message = 'Some syntax error..'
        mock_load.side_effect = SyntaxError(error_message)
        with self.assertRaises(Exception) as cm:
            config.get()
        assert_exception(self, cm, config.ConfigError, config._JSON_SYNTAX_ERROR.format(error_message))

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__loaded_config_gets_validated(self, mock_validate, mock_load):
        dummy_config = dict(config._default_config)
        mock_load.return_value = dummy_config
        config.get()
        mock_validate.assert_called_with(dummy_config)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__missing_mandatory_key__raises_config_error(self, mock_validate, mock_load):
        error_message = 'projects-path'
        mock_validate.side_effect = KeyError(error_message)
        with self.assertRaises(Exception) as cm:
            config.get()
        assert_exception(self, cm, config.ConfigError, config._MANDATORY_KEY_ERROR.format(error_message))

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__missing_optional_key__gets_replaced_with_the_default_value(self, mock_validate, mock_load):
        dummy_config = dict(config._default_config)
        del dummy_config['doc-width']
        mock_load.return_value = dummy_config
        expected = 80
        result = config.get()
        self.assertEqual(expected, result['doc-width'])


    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__invalid_key__raises_config_error(self, mock_validate, mock_load):
        dummy_config = dict(config._default_config)
        mock_load.return_value = dummy_config
        error_message = 'invalid-key'
        mock_validate.side_effect = SyntaxError(error_message)
        with self.assertRaises(Exception) as cm:
            config.get()
        assert_exception(self, cm, config.ConfigError, config._INVALID_KEY_ERROR.format(error_message))

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__invalid_value_for_key__raises_config_error(self, mock_validate, mock_load):
        dummy_config = dict(config._default_config)
        mock_load.return_value = dummy_config
        error_message = 'key'
        mock_validate.side_effect = ValueError(error_message)
        with self.assertRaises(Exception) as cm:
            config.get()
        assert_exception(self, cm, config.ConfigError, config._INVALID_VALUE_ERROR.format(error_message))
