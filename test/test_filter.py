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
                'string': init[0],
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
                'string': init[0],
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
                'string': init[0],
                'selection': (
                    (2,3),
                    (3,4)
                )
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)

    def test__sorting_works_for_two_items(self):
        init = [
            'def',
            'abc'
        ]
        f = filter.Filter(init)
        key = 'a'
        expected = [
            {
                'string': init[1],
                'selection': (
                    (0,1),
                )
            },
            {
                'string': init[0],
                'selection': ()
            }
        ]
        result = f.add_key(key)
        self.assertEqual(expected, result)

    def test__sorting_works_for_three_items(self):
        init = [
            'b_c_faef',
            'b_a_deef',
            'b_g_dgae'
        ]
        f = filter.Filter(init)
        key = 'ae'
        expected = [
            {
                'string': init[1],
                'selection': (
                    (2,3),
                    (5,6)
                )
            },
            {
                'string': init[0],
                'selection': (
                    (5,6),
                    (6,7)
                )
            },
            {
                'string': init[2],
                'selection': (
                    (6,7),
                    (7,8)
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


class WeightStringGeneration(TestCase):
    def test__generate_weigth_conversion_sring_from_positions_case_1(self):
        item = {
            'string': 'a',
            'selection': (
                (0,1),
            )
        }
        expected = '1'
        result = filter.weight_string_for_item(item)
        self.assertEqual(expected, result)

    def test__generate_weigth_conversion_sring_from_positions_case_2(self):
        item = {
            'string': 'aa',
            'selection': (
                (0,1),
            )
        }
        expected = '10'
        result = filter.weight_string_for_item(item)
        self.assertEqual(expected, result)

    def test__generate_weigth_conversion_sring_from_positions_case_3(self):
        item = {
            'string': 'aa',
            'selection': (
                (0,2),
            )
        }
        expected = '11'
        result = filter.weight_string_for_item(item)
        self.assertEqual(expected, result)

    def test__generate_weigth_conversion_sring_from_positions_case_4(self):
        item = {
            'string': 'aabbc',
            'selection': (
                (0,1),
                (2,3),
            )
        }
        expected = '10100'
        result = filter.weight_string_for_item(item)
        self.assertEqual(expected, result)

    def test__generate_weigth_conversion_sring_from_positions_case_5(self):
        item = {
            'string': 'aabbc',
            'selection': (
                (0,1),
                (2,5),
            )
        }
        expected = '10111'
        result = filter.weight_string_for_item(item)
        self.assertEqual(expected, result)


class ItemWeighting(TestCase):
    def test__weight_can_converted_to_number_case_1(self):
        item = {
            'string': 'aa',
            'selection': (
                (0,1),
            )
        }
        expected = 2
        result = filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__weight_can_converted_to_number_case_2(self):
        item = {
            'string': 'aabbc',
            'selection': (
                (0,1),
                (2,5),
            )
        }
        expected = 23
        result = filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

