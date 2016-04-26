#!/usr/bin/env python
# -*- coding: utf-8 -*-


from projects import paths




def main(args):
    projects_path = os.path.normpath(os.path.expanduser('~/projects'))

    if paths.inside_project(projects_path):
        print('Inside')
    else:
        print('Outside')

    dirs = list_dir_for_path('~')

    print(dirs)
