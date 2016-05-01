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

API:
    get()           Returns the validated configuration as a dictionary. In case of error throws
                    a ConfigError with a displayable error message.

Raises:
    ConfigError     in case of config related problems:
                        - invalid project file json syntax
                        - missing mandatory project file key
                        - invalid project file value
                        - invalid project file key
                        - project file cannot be written if missing
"""

import os
import json


class ConfigError(Exception):
    pass


def get():
    """ Only API function for the config module.


    :return: {dict}     loaded validated configuration.
    """
    config = {}
    try:
        config = _load_config()
    except IOError:
        try:
            _create_default_config()
            config = _load_config()
        except IOError as e:
            raise ConfigError('Config file ({}) cannot be created. '
                              'IOError: {}'.format(_config_file, e.args[0]))
    except SyntaxError as e:
        raise ConfigError('Invalid JSON format in config file ({}). '
                          'SyntaxError: {}'.format(_config_file, e.args[0]))

    try:
        _validate(config)
    except KeyError as e:
        raise ConfigError('Missing mandatory key "{}" '
                          'in config file ({}).'.format(e.args[0], _config_file))
    except SyntaxError as e:
        raise ConfigError('Invalid key "{}" '
                          'in config file ({}).'.format(e.args[0], _config_file))
    except ValueError as e:
        raise ConfigError('Invalid value for key "{}" '
                          'in config file ({}).'.format(e.args[0], _config_file))
    return config


_config_file = '~/.prc'

_default_config = {
    'projects-path': '~/projects'
}

_optional_config = {
    'number-color': 'yellow',
    'highlight-color': 'yellow',
    'plugins': []
}


def _get_config_path():
    return os.path.expanduser(_config_file)


def _load_config():
    """ Config loading
    Raises:
        IOError         on missing config file
        SyntaxError     on invalid json syntax
    :return: {dict} loaded but unvalidated config
    """
    config_path = _get_config_path()
    with open(config_path, 'r') as f:
        return json.load(f)


def _validate(config):
    """ Config validation
    Raises:
        KeyError        on missing mandatory key
        SyntaxError     on invalid key
        ValueError      on invalid value for key
    :param config: {dict} config to validate
    :return: None
    """
    for mandatory_key in _default_config.keys():
        if mandatory_key not in config:
            raise KeyError(mandatory_key)
    full_config = _default_config.copy()
    full_config.update(_optional_config)
    for key in config.keys():
        if key not in full_config:
            raise SyntaxError(key)
        elif not isinstance(config[key], full_config[key].__class__):
            raise ValueError(key)


def _create_default_config():
    """ Writes the full default configuration to the appropriate place.
    Raises:
        IOError  - on unsuccesful file write
    :return: None
    """
    config_path = _get_config_path()
    full_config = _default_config.copy()
    full_config.update(_optional_config)
    with open(config_path, 'w+') as f:
        json.dump(f, full_config)
