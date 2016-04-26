#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def list_dir_for_path(path):
    return os.listdir(os.path.expanduser(path))


def inside_project(projects_path):
    current_path = os.getcwd()
    if projects_path == current_path:
        return False
    else:
        return current_path.startswith(projects_path)