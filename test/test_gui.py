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

from projects import gui


class StringGeneration(TestCase):
    def test__display_string_can_be_generated_for_single_line_no_highlight(self):
        data = [
            [
                {
                    'string': 'abc',
                    'highlight': False
                }
            ]
        ]
        expected = [
            ('text', 'abc'), ('text', '\n')
        ]
        result = gui.generate_gui_string(data, 'text', 'highlight')
        self.assertEqual(expected, result)

    def test__display_string_with_highlight(self):
        data = [
            [
                {
                    'string': 'a',
                    'highlight': False
                },
                {
                    'string': 'b',
                    'highlight': True
                },
                {
                    'string': 'c',
                    'highlight': False
                }
            ]
        ]
        expected = [
            ('text', 'a'), ('highlight', 'b'), ('text', 'c'), ('text', '\n')
        ]
        result = gui.generate_gui_string(data, 'text', 'highlight')
        self.assertEqual(expected, result)