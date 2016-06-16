#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from projects.projectfile import utils


class AdditionalHelperFunctions(TestCase):
    def test__get_currently_parsable_command(self):
        data = {
            'commands': {
                'current-command': {
                    'done': False
                },
                'finished-command': {
                    'done': True
                }
            }
        }
        expected = data['commands']['current-command']
        result = utils.get_current_command(data)
        self.assertEqual(expected, result)

    def test__alternative_commands_can_be_handled(self):
        data = {
            'commands': {
                'my_command': {
                    'done': False,
                    'post': ['some command']
                },
                'alternative': {
                    'alias': 'my_command'
                }
            }
        }
        expected = data['commands']['my_command']
        result = utils.get_current_command(data)
        self.assertEqual(expected, result)

    def test__no_returnable_command_found__returns_none(self):
        data = {
            'commands': {
                'current-command': {
                    'done': True
                },
                'finished-command': {
                    'done': True
                }
            }
        }
        expected = None
        result = utils.get_current_command(data)
        self.assertEqual(expected, result)