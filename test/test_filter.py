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

    def test__sorting_works_for_three_items(self):
        init = [
            'b_c_faef',
            'b_a_deef',
            'b_g_dgae'
        ]
        f = filter.Filter(init)
        expected = [
            [
                {
                    'string': 'b_',
                    'highlight': False
                },
                {
                    'string': 'a',
                    'highlight': True
                },
                {
                    'string': '_d',
                    'highlight': False
                },
                {
                    'string': 'e',
                    'highlight': True
                },
                {
                    'string': 'ef',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'b_c_f',
                    'highlight': False
                },
                {
                    'string': 'ae',
                    'highlight': True
                },
                {
                    'string': 'f',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'b_g_dg',
                    'highlight': False
                },
                {
                    'string': 'ae',
                    'highlight': True
                }
            ]
        ]
        f.add_key('a')
        f.add_key('e')
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
        # binary 10 = 2
        expected = 2/2   # 2 / len(2)
        filter.weight_item(item)
        self.assertEqual(expected, item['weight'])

    def test__weight_can_converted_to_number_case_2(self):
        item = {
            'string': 'aabbc',
            'selection': (
                (0,1),
                (2,5),
            )
        }
        # binary 10111 = 23
        expected = 23/5  # 23 / len(string)
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