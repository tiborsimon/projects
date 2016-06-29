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
import yaml


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
            raise ConfigError(_FILE_CREATION_ERROR.format(e.args[0]))
    except SyntaxError as e:
        raise ConfigError(_JSON_SYNTAX_ERROR.format(e.args[0]))
    except Exception:
        raise ConfigError(_JSON_SYNTAX_ERROR.format('Yaml syntax error..'))

    try:
        _validate(config)
    except KeyError as e:
        raise ConfigError(_MANDATORY_KEY_ERROR.format(e.args[0]))
    except SyntaxError as e:
        raise ConfigError(_INVALID_KEY_ERROR.format(e.args[0]))
    except ValueError as e:
        raise ConfigError(_INVALID_VALUE_ERROR.format(e.args[0]))

    config['projects-path'] = os.path.expanduser(config['projects-path'])
    _complete_config(config)
    return config


_CONFIG_FILE = '~/.prc'
_FILE_CREATION_ERROR = 'Config file ({}) cannot be created. IOError: {{}}'.format(_CONFIG_FILE)
_JSON_SYNTAX_ERROR = 'Invalid Yaml format in config file ({}). SyntaxError: {{}}'.format(_CONFIG_FILE)
_MANDATORY_KEY_ERROR = 'Missing mandatory key "{{}}" in config file ({}).'.format(_CONFIG_FILE)
_INVALID_KEY_ERROR = 'Invalid key "{{}}" in config file ({}).'.format(_CONFIG_FILE)
_INVALID_VALUE_ERROR = 'Invalid value for key "{{}}" in config file ({}).'.format(_CONFIG_FILE)

_default_config = {
    'projects-path': '~/projects',
    'doc-width': 80
}

_mandatory_keys = [
    'projects-path'
]

_optional_keys = [
    'doc-width'
]


def _complete_config(config):
    for key in _optional_keys:
        if key not in config:
            config[key] = _default_config[key]


def _get_config_path():
    return os.path.expanduser(_CONFIG_FILE)


def _load_config():
    """ Config loading
    Raises:
        IOError         on missing config file
        SyntaxError     on invalid json syntax
    :return: {dict} loaded but unvalidated config
    """
    config_path = _get_config_path()
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def _validate(config):
    """ Config validation
    Raises:
        KeyError        on missing mandatory key
        SyntaxError     on invalid key
        ValueError      on invalid value for key
    :param config: {dict} config to validate
    :return: None
    """
    for mandatory_key in _mandatory_keys:
        if mandatory_key not in config:
            raise KeyError(mandatory_key)
    for key in config.keys():
        if key not in _mandatory_keys and key not in _optional_keys:
            raise SyntaxError(key)
        if not isinstance(config[key], _default_config[key].__class__):
            raise ValueError(key)


def _create_default_config():
    """ Writes the full default configuration to the appropriate place.
    Raises:
        IOError  - on unsuccesful file write
    :return: None
    """
    config_path = _get_config_path()
    with open(config_path, 'w+') as f:
        yaml.dump(_default_config, f, default_flow_style=False)

