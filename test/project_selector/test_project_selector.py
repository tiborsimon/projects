#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects.gui import project_selector


class ProjectSelectorBaseCases(TestCase):
    def test__project_selector_can_be_initialized(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        self.assertEqual(data, selector.data)
        self.assertEqual('', selector.keys)
        self.assertEqual(0, selector.focus)

    def test__focus_can_be_moved_down(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        self.assertEqual(0, selector.focus)
        selector.down()
        self.assertEqual(1, selector.focus)

    def test__focus_has_lower_limit(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        selector.down()
        selector.down()
        self.assertEqual(2, selector.focus)
        selector.down()
        self.assertEqual(2, selector.focus)

    def test__focus_can_be_moved_up(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        self.assertEqual(0, selector.focus)
        selector.down()
        selector.up()
        self.assertEqual(0, selector.focus)

    def test__focus_has_upper_limit(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        self.assertEqual(0, selector.focus)
        selector.down()
        selector.up()
        self.assertEqual(0, selector.focus)
        selector.up()
        self.assertEqual(0, selector.focus)

    def test__data_in_focus_will_be_returned_on_selection_from_the_filtered_list(self):
        data = [
            'a',
            'b',
            'c'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        selector.down()
        expected = 'b'
        result = selector.select()
        self.assertEqual(expected, result)

    def test__adding_key_is_only_possible_if_there_are_match(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        self.assertEqual('', selector.keys)
        selector.add_key('a')
        self.assertEqual('', selector.keys)
        selector.add_key('o')
        self.assertEqual('o', selector.keys)
        selector.add_key('e')
        self.assertEqual('oe', selector.keys)
        selector.add_key('l')
        self.assertEqual('oe', selector.keys)

    def test__removing_key(self):
        data = [
            'one',
            'two',
            'three'
        ]
        selector = project_selector.ProjectSelector(data, '', '', '')
        selector.add_key('o')
        selector.remove_key()
        self.assertEqual('', selector.keys)
        selector.remove_key()
        self.assertEqual('', selector.keys)

