#!/usr/bin/env python
# -*- coding: utf-8 -*-

from projects import paths
from projects import config


def main(args):
    try:
        conf = config.get()
        print(conf)
    except:
        pass
    if paths.inside_project(conf['projects-path']):
        print('Inside')
        pass
    else:
        print('Outside')
        pass

if __name__ == '__main__':
    main('hello')

