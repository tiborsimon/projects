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

from projects import config


class Path(TestCase):

    @mock.patch.object(config, 'os', autospec=True)
    def test__path_expanded_correctly(self, mock_os):
        config._get_config_path()
        mock_os.path.expanduser.assert_called_with('~/.prc')


class Loading(TestCase):

    @mock.patch.object(config, 'json', autospec=True)
    @mock.patch.object(config, 'os', autospec=True)
    def test__config_path_required_correctly(self, mock_os, mock_json):
        with mock.patch(open_mock_string):
            config._load_config()
        mock_os.path.expanduser.assert_called_with(config._config_file)

    @mock.patch.object(config, 'json', autospec=True)
    @mock.patch.object(config, '_get_config_path', autospec=True)
    def test__config_file_is_opened_from_the_right_path(self, mock_path, mock_json):
        dummy_config_path = '/config/path'
        mock_path.return_value = dummy_config_path
        with mock.patch(open_mock_string) as mock_open:
            config._load_config()
            mock_open.assert_called_with(dummy_config_path, 'r')

    @mock.patch.object(config, 'json', autospec=True)
    def test__file_not_found__raises_error(self, mock_json):
        mock_open = mock.MagicMock(side_effect = IOError())
        with self.assertRaises(Exception) as cm:
            with mock.patch(open_mock_string, mock_open):
                config._load_config()
        self.assertEqual(cm.exception.__class__, IOError)

    @mock.patch.object(config, 'json', autospec=True)
    def test__parsed_config_file_is_returned(self, mock_json):
        dummy_config = {'dummy': 'config'}
        mock_json.load.return_value = dummy_config
        with mock.patch(open_mock_string):
            result = config._load_config()
        self.assertEqual(dummy_config, result)

    @mock.patch.object(config, 'json', autospec=True)
    def test__invalid_json_syntax__raises_error(self, mock_json):
        mock_json.load.side_effect = SyntaxError('json invalid')
        with self.assertRaises(Exception) as cm:
            with mock.patch(open_mock_string):
                config._load_config()
        self.assertEqual(cm.exception.__class__, SyntaxError)


class Validation(TestCase):

    def test__mandatory_keys_present__no_exception_raised(self):
        dc = config._default_config
        config._validate(dc)

    def test__missing_mandatory_key__raises_key_error(self):
        with self.assertRaises(Exception) as cm:
            dummy_config = {}
            config._validate(dummy_config)
        self.assertEqual(cm.exception.__class__, KeyError)

    def test__invalid_key__raises_syntax_error(self):
        invalid_config = {
            'projects-path': '~/projects',
            'selection-mode-index-not-fuzzy': True,
            'invalid-key': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        self.assertEqual(cm.exception.__class__, SyntaxError)

    def test__invalid_value__raises_value_error(self):
        invalid_config = {
            'projects-path': 42
        }
        with self.assertRaises(Exception) as cm:
            config._validate(invalid_config)
        self.assertEqual(cm.exception.__class__, ValueError)


class Creation(TestCase):

    @mock.patch.object(config, '_get_config_path', autospec=True)
    @mock.patch.object(config, 'json', autospec=True)
    def test__config_is_written_to_the_right_place(self, mock_json, mock_path):
        dummy_path = '/config/path'
        mock_path.return_value = dummy_path
        with mock.patch(open_mock_string) as mock_open:
            config._create_default_config()
            mock_open.assert_called_with(dummy_path, 'w+')

    @mock.patch.object(config, '_get_config_path', autospec=True)
    @mock.patch.object(config, 'json', autospec=True)
    def test__file_cannot_be_written__raises_error(self, mock_json, mock_path):
        with mock.patch(open_mock_string) as mock_open:
            mock_open.side_effect = IOError()
            with self.assertRaises(Exception) as cm:
                config._create_default_config()
            self.assertEqual(cm.exception.__class__, IOError)

    @mock.patch.object(config, 'json', autospec=True)
    def test__json_file_is_written_with_the_full_configuration(self, mock_json):
        full_config = config._default_config.copy()
        full_config.update(config._optional_config)
        mock_open = mock.mock_open()
        with mock.patch(open_mock_string, mock_open):
            config._create_default_config()
        mock_json.dump.assert_called_with(mock_open.return_value, full_config)


class Getter(TestCase):

    @mock.patch.object(config, '_load_config', autospec=True)
    def test__loaded_config_returned(self, mock_load):
        dummy_config = config._default_config
        mock_load.return_value = dummy_config
        result = config.get()
        self.assertEqual(dummy_config, result)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_create_default_config', autospec=True)
    def test__config_file_not_exits__creates_new_one(self, mock_create, mock_load):
        mock_load.side_effect = [IOError(), config._default_config]
        config.get()
        mock_create.assert_called_with()

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_create_default_config', autospec=True)
    def test__config_file_cannot_be_written__raises_config_error(self, mock_create, mock_load):
        mock_load.side_effect = IOError()
        mock_create.side_effect = IOError('Some error..')
        with self.assertRaises(Exception) as cm:
            config.get()
        self.assertEqual(cm.exception.__class__, config.ConfigError)
        self.assertTrue('Config file ({}) cannot be created. '
                        'IOError: Some error..'.format(config._config_file) in cm.exception)

    @mock.patch.object(config, '_load_config', autospec=True)
    def test__invalid_json_syntax__raises_config_error(self, mock_load):
        mock_load.side_effect = SyntaxError('Some syntax error..')
        with self.assertRaises(Exception) as cm:
            config.get()
        self.assertEqual(cm.exception.__class__, config.ConfigError)
        self.assertTrue('Invalid JSON format in config file ({}). '
                        'SyntaxError: Some syntax error..'.format(config._config_file) in cm.exception)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__loaded_config_gets_validated(self, mock_validate, mock_load):
        dummy_config = config._default_config
        mock_load.return_value = dummy_config
        config.get()
        mock_validate.assert_called_with(dummy_config)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__missing_mandatory_key__raises_config_error(self, mock_validate, mock_load):
        mock_validate.side_effect = KeyError('projects-path')
        with self.assertRaises(Exception) as cm:
            config.get()
        self.assertEqual(cm.exception.__class__, config.ConfigError)
        self.assertTrue('Missing mandatory key "projects-path" '
                        'in config file ({}).'.format(config._config_file) in cm.exception)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__invalid_key__raises_config_error(self, mock_validate, mock_load):
        mock_validate.side_effect = SyntaxError('invalid-key')
        with self.assertRaises(Exception) as cm:
            config.get()
        self.assertEqual(cm.exception.__class__, config.ConfigError)
        self.assertTrue('Invalid key "invalid-key" '
                        'in config file ({}).'.format(config._config_file) in cm.exception)

    @mock.patch.object(config, '_load_config', autospec=True)
    @mock.patch.object(config, '_validate', autospec=True)
    def test__invalid_value_for_key__raises_config_error(self, mock_validate, mock_load):
        mock_validate.side_effect = ValueError('key')
        with self.assertRaises(Exception) as cm:
            config.get()
        self.assertEqual(cm.exception.__class__, config.ConfigError)
        self.assertTrue('Invalid value for key "key" '
                        'in config file ({}).'.format(config._config_file) in cm.exception)
