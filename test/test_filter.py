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


class FilterTestsAPI(TestCase):
    def test__filter_can_be_initialized(self):
        input = [
            'item 1',
            'item 2'
        ]
        f = filter.Filter(input)

    def test__no_match_returns_empty_selection(self):
        init = [
            'abc'
        ]
        f = filter.Filter(init)
        key = 'd'
        expected = [
            {
                'line': init[0],
                'selection': ()
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)

    def test__result_for_one_line_with_one_match(self):
        init = [
            'abcd'
        ]
        f = filter.Filter(init)
        key = 'c'
        expected = [
            {
                'line': init[0],
                'selection': (
                    (2,3),
                )
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)

    def test__result_for_one_line_with_two_matches(self):
        init = [
            'abcdc'
        ]
        f = filter.Filter(init)
        key = 'cd'
        expected = [
            {
                'line': init[0],
                'selection': (
                    (2,3),
                    (3,4)
                )
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)

class SearchPatternGeneration(TestCase):
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

class SortAlgorithm(TestCase):
    def test__one_long_line__first_character_match__returns_zero(self):
        item = {
            'line': 'a',
            'selection': (
                (0,1),
            )
        }
        expected = 0
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__two_long_line__all_character_match__returns_zero(self):
        item = {
            'line': 'aa',
            'selection': (
                (0,2),
            )
        }
        expected = 0
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__three_long_line__all_character_match__returns_zero(self):
        item = {
            'line': 'aaa',
            'selection': (
                (0,3),
            )
        }
        expected = 0
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__three_long_line__first_two_characters_match__returns_zero(self):
        item = {
            'line': 'aaa',
            'selection': (
                (0,2),
            )
        }
        expected = 1
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

