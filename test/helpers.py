#!/usr/bin/env python
# -*- coding: utf-8 -*-


def assert_exception_type(self, cm, exception):
    self.assertEqual(cm.exception.__class__, exception)


def assert_exception_text(self, cm, text):
    self.assertTrue(text == cm.exception.args[0])


def assert_exception(self, cm, exception, text):
    assert_exception_type(self, cm, exception)
    assert_exception_text(self, cm, text)
