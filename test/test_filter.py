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

from projects import filter


class FilterTests(TestCase):
    def test__filter_can_be_initialized(self):
        input = [
            'item 1',
            'item 2'
        ]
        f = filter.Filter(input)

    def test__pattern_generation_1(self):
        keys = 'c'
        expected = '[^c]*(c)'
        result = filter._get_pattern(keys)
        self.assertEqual(expected, result)

    def test__pattern_generation_2(self):
        keys = 'cde'
        expected = '[^c]*(c)[^d]*(d)[^e]*(e)'
        result = filter._get_pattern(keys)
        self.assertEqual(expected, result)

    def test__filter_reacts_to_the_first_letter(self):
        init = [
            'abcd'
        ]
        f = filter.Filter(init)
        key = 'c'
        expected = [
            {
                'item': 'abcd',
                'selection': [
                    (2,3)
                ]
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)