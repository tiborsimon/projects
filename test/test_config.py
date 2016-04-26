#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import mock
import os

from projects import config


class ConfigTestCases(TestCase):

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    @mock.patch('__builtin__.open')
    def test__config_path_required_correctly(self, mock_open, mock_os, mock_json):
        config.get_config()
        mock_os.path.expanduser.assert_called_with('~/.prc')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    @mock.patch('__builtin__.open')
    def test__config_file_is_opened_from_the_right_path(self, mock_open, mock_os, mock_json):
        dummy_config_path = '/config/path'
        mock_os.path.expanduser.return_value = dummy_config_path
        config.get_config()
        mock_open.assert_called_with(dummy_config_path, 'r')

    @mock.patch('projects.config.json')
    @mock.patch('projects.config.os')
    @mock.patch('__builtin__.open')
    def test__file_not_found__raises_error(self, mock_open, mock_os, mock_json):
        mock_open.side_effect = IOError('cannot open file')
        with self.assertRaises(IOError):
            config.get_config()

    @mock.patch('projects.config.json')
    @mock.patch('__builtin__.open')
    def test__parsed_config_file_is_returned(self, mock_open, mock_json):
        dummy_config = {
            'dummy': 'config'
        }
        mock_json.load.return_value = dummy_config
        result = config.get_config()
        self.assertEqual(dummy_config, result)

    @mock.patch('projects.config.json')
    @mock.patch('__builtin__.open')
    def test__invalid_json_syntax__raises_error(self, mock_open, mock_json):
        mock_json.load.side_effect = SyntaxError('json invalid')
        with self.assertRaises(SyntaxError):
            config.get_config()