#!/usr/bin/env python
# -*- coding: utf-8 -*-

from projects import paths


def main(args):
    if paths.inside_project(projects_path):
        print('Inside')
    else:
        print('Outside')
