#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects import project_selector


class Rendering(TestCase):
    def test__single_item_no_selection(self):
        data = [
            [
                {
                    'string': 'abc',
                    'highlight': False
                }
            ]
        ]
        index = 0
        normal = 'n'
        highlighted = 'h'
        selected = 's'
        expected = [
            (selected, '[ '), (normal, 'abc'), (selected, ' ]'), (normal, '\n')
        ]
        result = project_selector.render_string(data, index, normal, highlighted, selected)
        self.assertEqual(expected, result)

    def test__single_item_with_selection(self):
        data = [
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
        index = 0
        normal = 'n'
        highlighted = 'h'
        selected = 's'
        expected = [
            (selected, '[ '), (normal, 'ab'), (highlighted, 'c'), (selected, ' ]'), (normal, '\n')
        ]
        result = project_selector.render_string(data, index, normal, highlighted, selected)
        self.assertEqual(expected, result)

    def test__two_items_no_selection(self):
        data = [
            [
                {
                    'string': 'a',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'b',
                    'highlight': False
                }
            ]
        ]
        index = 0
        normal = 'n'
        highlighted = 'h'
        selected = 's'
        expected = [
            (selected, '[ '), (normal, 'a'), (selected, ' ]'), (normal, '\n'),
            (normal, '  '), (normal, 'b'), (normal, '\n')
        ]
        result = project_selector.render_string(data, index, normal, highlighted, selected)
        self.assertEqual(expected, result)

    def test__two_items_no_selection_index_moved(self):
        data = [
            [
                {
                    'string': 'a',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'b',
                    'highlight': False
                }
            ]
        ]
        index = 1
        normal = 'n'
        highlighted = 'h'
        selected = 's'
        expected = [
            (normal, '  '), (normal, 'a'), (normal, '\n'),
            (selected, '[ '), (normal, 'b'), (selected, ' ]'), (normal, '\n')
        ]
        result = project_selector.render_string(data, index, normal, highlighted, selected)
        self.assertEqual(expected, result)

    def test__two_items_no_selection_index_moved_with_selection(self):
        data = [
            [
                {
                    'string': 'a',
                    'highlight': False
                }
            ],
            [
                {
                    'string': 'b',
                    'highlight': False
                },
                {
                    'string': 'c',
                    'highlight': True
                }
            ]
        ]
        index = 1
        normal = 'n'
        highlighted = 'h'
        selected = 's'
        expected = [
            (normal, '  '), (normal, 'a'), (normal, '\n'),
            (selected, '[ '), (normal, 'b'), (highlighted, 'c'), (selected, ' ]'), (normal, '\n')
        ]
        result = project_selector.render_string(data, index, normal, highlighted, selected)
        self.assertEqual(expected, result)