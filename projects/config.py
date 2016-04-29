#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the configuration management functions. It handles the configuration
file (~/.prc) and configuration folder (~/.p). The configuration file contains the
projects root path. This is the only mandatory settings the user should have.

There are optional parameters as well:

    number-color      Color of the project indexes.
    highlight-color   Color of the currently selected item.

        possible colors: red, green, yellow, blue, magenta, cyan, white

    plugins           Projects contains an extensive plugin system. You can define here
                      your custom projects in a list, and put the project files into the
                      ~/.p/plugins directory.

"""

import os
import json

default_config = {
    'projects-path': '~/projects'
}

optional_config = {
    'number-color': 'yellow',
    'highlight-color': 'yellow',
    'plugins': []
}

def get_config_path():
    return os.path.expanduser('~/.prc')


def load_config():
    """ Config loading
    Raises:
        IOError     - on missing config file
        SyntaxError - on invalid json syntax
    :return: {dict} loaded but unvalidated config
    """
    config_path = get_config_path()
    with open(config_path, 'r') as f:
        return json.load(f)


def validate(config):
    """ Config validation
    Raises:
        KeyError    - on missing mandatory key
        SyntaxError - on invalid key
        ValueError  - on invalid value for key
    :param config: {dict} config to validate
    :return: None
    """
    for mandatory_key in default_config.keys():
        if mandatory_key not in config:
            raise KeyError(mandatory_key)
    full_config = default_config.copy()
    full_config.update(optional_config)
    for key in config.keys():
        if key not in full_config:
            raise SyntaxError(key)
        elif not isinstance(config[key], full_config[key].__class__):
            raise ValueError(key)


def create_default_config():
    """ Writes the full default configuration to the appropriate place.
    :return: None
    """
    config_path = get_config_path()
    full_config = default_config.copy()
    full_config.update(optional_config)
    with open(config_path, 'w+') as f:
        json.dump(f, full_config)


def get():
    config = {}
    try:
        config = load_config()
        validate(config)
    except Exception as e:
        # TODO: add call to error display
        try:
            create_default_config()
            current_config = load_config()
        except IOError:
            # TODO: cannot create default config
            pass
    return config

