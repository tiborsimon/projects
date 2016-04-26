#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json


def get_config():
    config_path = os.path.expanduser('~/.prc')
    with open(config_path, 'r') as f:
        return json.load(f)
