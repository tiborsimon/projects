#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def list_dir_for_path(path):
    dirs = os.listdir(os.path.expanduser(path))
    return [d for d in dirs if not d.startswith('.')]


def inside_project(projects_path):
    current_path = os.getcwd()
    if projects_path == current_path:
        return False
    else:
        return current_path.startswith(projects_path)


def get_project_root(projects_root, current_path):
    separator = os.path.sep
    root = projects_root.split(separator)
    current = current_path.split(separator)
    ret = {
        'path': os.path.join(projects_root, current[len(root)]),
        'name': current[len(root)]
    }
    return ret

