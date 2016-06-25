#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects import doc_generator


class DocLineWrapping(TestCase):
    def test__long_lines_can_be_wrapped(self):
        raw = 'This is a very nice project.. This is a very nice project.. This is a very nice project. .his is a very nice project..\n\nThis is a very nice project.. This is a very nice project.. This is a very nice project. .his is a very nice project.. Which has a very nice line..'
        width = 80
        expected = '    This is\n    a long\n    line..'
        result = doc_generator.wrap_lines(raw, width)
        self.assertEqual(expected, result)

# class DocOutputTests(TestCase):
#     def test__