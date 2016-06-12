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

    def test__no_match_returns__whole_string__without_highlight(self):
        init = [
            'abc'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'abc',
                    'highlight': False
                }
            ]
        ]
        f.add_key('d')
        result = f.filter()
        self.assertEqual(expected, result)

    def test__result_for_one_line_with_one_match(self):
        init = [
            'abcd'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'ab',
                    'highlight': False
                },
                {
                    'string': 'c',
                    'highlight': True
                },
                {
                    'string': 'd',
                    'highlight': False
                }
            ]
        ]
        f.add_key('c')
        result = f.filter()
        self.assertEqual(expected, result)

    def test__result_for_one_line_with_two_matches(self):
        init = [
            'abcdc'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'ab',
                    'highlight': False
                },
                {
                    'string': 'cd',
                    'highlight': True
                },
                {
                    'string': 'c',
                    'highlight': False
                }
            ]
        ]
        f.add_key('c')
        f.add_key('d')
        result = f.filter()
        self.assertEqual(expected, result)

    def test__sorting_works_for_two_items(self):
        init = [
            'def',
            'abc'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': 'bc',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'def',
                    'highlight': False
                }
            ]
        ]
        f.add_key('a')
        result = f.filter()
        self.assertEqual(expected, result)

    def test__equal_weight_sorted_by_alphabet(self):
        init = [
            'a_d',
            'a_b',
            'a_c'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': '_b',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': '_c',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': '_d',
                    'highlight': False
                }
            ]
        ]
        f.add_key('a')
        result = f.filter()
        self.assertEqual(expected, result)


    def test__adding_then_removing_keys(self):
        init = [
            'abcdc'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'ab',
                    'highlight': False
                },
                {
                    'string': 'cd',
                    'highlight': True
                },
                {
                    'string': 'c',
                    'highlight': False
                }
            ]
        ]
        f.add_key('a')
        f.remove_key()
        f.add_key('c')
        f.add_key('d')
        f.add_key('k')
        f.remove_key()
        result = f.filter()
        self.assertEqual(expected, result)


class SearchPatternGeneration(TestCase):
    def test__pattern_generation_1(self):
        keys = 'a'
        expected = ['(a)']
        result = filter._get_pattern_list(keys)
        self.assertEqual(expected, result)

    def test__pattern_generation_2(self):
        keys = 'ab'
        expected = [
            '(ab)',
            '(a)(b)'
        ]
        result = filter._get_pattern_list(keys)
        self.assertEqual(expected, result)

    def test__pattern_generation_3(self):
        keys = 'abc'
        expected = [
            '(abc)',
            '(ab)(c)',
            '(a)(b)(c)'
        ]
        result = filter._get_pattern_list(keys)
        self.assertEqual(expected, result)


class ItemWeighting(TestCase):
    def test__no_match_results_zero_weight(self):
        item = {
            'string': 'abc',
            'selection': ()
        }
        expected = 100000000000
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__single_in_the_first_character__returns_zero(self):
        item = {
            'string': 'abc',
            'selection': ((0,1),)
        }
        expected = 0
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__single_match_in_the_second_position(self):
        item = {
            'string': 'abc',
            'selection': ((1, 2),)
        }
        expected = 1
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__single_match_in_the_tenth_position(self):
        item = {
            'string': 'abc',
            'selection': ((9, 10),)
        }
        expected = 9
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])


class Transformation(TestCase):
    def test__transformation_with_no_selection__returns_the_whole_line(self):
        data = [
            {
                'string': 'abc',
                'selection': ()
            }
        ]
        expected = [
            [
                {
                    'string': 'abc',
                    'highlight': False
                }
            ]
        ]
        result = filter.transform_data(data)
        self.assertEqual(expected, result)

    def test__transformation_with_single_selection_in_the_front(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                )
            }
        ]
        expected = [
            [
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': 'bc',
                    'highlight': False
                }
            ]
        ]
        result = filter.transform_data(data)
        self.assertEqual(expected, result)

    def test__transformation_with_single_selection_in_the_middle(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (1, 2),
                )
            }
        ]
        expected = [
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
        result = filter.transform_data(data)
        self.assertEqual(expected, result)

    def test__transformation_with_single_selection_in_the_end(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (2, 3),
                )
            }
        ]
        expected = [
            [
                {
                    'string': 'ab',
                    'highlight': False
                },
                {
                    'string': 'c',
                    'highlight': True
                }
            ]
        ]
        result = filter.transform_data(data)
        self.assertEqual(expected, result)

    def test__transformation_with_full_word_selected(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 3),
                )
            }
        ]
        expected = [
            [
                {
                    'string': 'abc',
                    'highlight': True
                }
            ]
        ]
        result = filter.transform_data(data)
        self.assertEqual(expected, result)

    def test__transformation_with_two_selections(self):
        data = [
            {
                'string': 'abcdef',
                'selection': (
                    (1, 2),
                    (3, 5),
                )
            }
        ]
        expected = [
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
                },
                {
                    'string': 'de',
                    'highlight': True
                },
                {
                    'string': 'f',
                    'highlight': False
                }
            ]
        ]
        result = filter.transform_data(data)
        self.assertEqual(expected, result)


class SelectionMerge(TestCase):
    def test__no_selection_no_merge_needed(self):
        data = [
            {
                'string': 'abc',
                'selection': ()
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': ()
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__single_selection_no_merge_needed(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (1, 2),
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (1, 2),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__two_no_mergable_selections(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (1, 2),
                    (5, 6)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (1, 2),
                    (5, 6)
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__structure_with_selections_next_to_each_other_will_merged(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (1, 2)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (0, 2),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__item_before_the_merge(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (2, 3),
                    (3, 4)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (2, 4),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__item_after_the_merge(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (1, 2),
                    (3, 4)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (0, 2),
                    (3, 4),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__multiple_merges(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (1, 2),
                    (3, 4),
                    (6, 7),
                    (7, 8)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (0, 2),
                    (3, 4),
                    (6, 8)
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__chaining_merges(self):
        data = [
            {
                'string': 'abc',
                'selection': (
                    (0, 1),
                    (1, 2),
                    (2, 3),
                    (3, 4),
                    (4, 5)
                )
            }
        ]
        expected = [
            {
                'string': 'abc',
                'selection': (
                    (0, 5),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__multiple_nodes_can_processed_no_yes(self):
        data = [
            {
                'string': 'no',
                'selection': ()
            },
            {
                'string': 'yes',
                'selection': (
                    (0, 1),
                    (1, 2)
                )
            }
        ]
        expected = [
            {
                'string': 'no',
                'selection': ()
            },
            {
                'string': 'yes',
                'selection': (
                    (0, 2),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__multiple_nodes_can_processed_yes_no(self):
        data = [
            {
                'string': 'yes',
                'selection': (
                    (0, 1),
                    (1, 2)
                )
            },
            {
                'string': 'no',
                'selection': ()
            }

        ]
        expected = [
            {
                'string': 'yes',
                'selection': (
                    (0, 2),
                )
            },
            {
                'string': 'no',
                'selection': ()
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__multiple_nodes_can_processed_yes_yes(self):
        data = [
            {
                'string': 'yes',
                'selection': (
                    (0, 1),
                    (1, 2)
                )
            },
            {
                'string': 'yes',
                'selection': (
                    (0, 1),
                    (1, 2)
                )
            }

        ]
        expected = [
            {
                'string': 'yes',
                'selection': (
                    (0, 2),
                )
            },
            {
                'string': 'yes',
                'selection': (
                    (0, 2),
                )
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)

    def test__multiple_nodes_can_processed_no_no(self):
        data = [
            {
                'string': 'no',
                'selection': ()
            },
            {
                'string': 'no',
                'selection': ()
            }

        ]
        expected = [
            {
                'string': 'no',
                'selection': ()
            },
            {
                'string': 'no',
                'selection': ()
            }
        ]
        filter.merge_neighbour_selections(data)
        self.assertEqual(expected, data)