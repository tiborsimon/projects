#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

default_config = {
    'projects-path': '~/projects',
    'selection-mode-index-not-fuzzy': True,
}

optional_keys = {
    'number-color': 'yellow',
    'selection-color': 'yellow',
    'plugins': []
}

current_config = {}


def load_config():
    config_path = os.path.expanduser('~/.prc')
    with open(config_path, 'r') as f:
        return json.load(f)


def create_default_config():
    config_path = os.path.expanduser('~/.prc')
    with open(config_path, 'w+') as f:
        json.dump(f, default_config)


def validate(config, default_config):
    for mandatory_key in default_config.keys():
        if mandatory_key not in config:
            raise KeyError(mandatory_key)
    full_config = dict(default_config)
    full_config.update(optional_keys)
    for key in config.keys():
        if key not in full_config:
            raise SyntaxError(key)


def init():
    global current_config
    try:
        current_config = load_config()
    except IOError:
        # TODO: add call to error display
        try:
            create_default_config()
            current_config = load_config()
        except IOError:
            # TODO: cannot create default config
    except
