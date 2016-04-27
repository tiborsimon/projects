#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json


default_config = {
    'projects-path': '~/projects',
    'selection-mode-index-not-fuzzy': True,
}


def get_config():
    config_path = os.path.expanduser('~/.prc')
    with open(config_path, 'r') as f:
        return json.load(f)


def validate(config):
    pass
