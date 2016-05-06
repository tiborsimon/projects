#!/usr/bin/env python
# -*- coding: utf-8 -*-

from projects import paths
from projects import config


def main(args):
    try:
        conf = config.get()
    except:
        pass
    if paths.inside_project(conf['projects-path']):
        # print('Inside')
        pass
    else:
        # print('Outside')
        pass
