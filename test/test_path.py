#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
try:
    import mock
except ImportError:
    from unittest import mock

from projects import paths


class DetermineIfCallHappenedFromProject(TestCase):

    @mock.patch('projects.paths.os')
    def test__current_path_gets_called(self, mock_os):
        paths.inside_project('some/path')
        mock_os.getcwd.assert_called_with()

    @mock.patch('projects.paths.os')
    def test__inside_projects_root__returns_false(self, mock_os):
        p = '/machine/projects'
        mock_os.getcwd.return_value = p
        result = paths.inside_project(p)
        self.assertEqual(False, result)

    @mock.patch('projects.paths.os')
    def test__outside_projects__returns_false(self, mock_os):
        p = '/machine/projects'
        mock_os.getcwd.return_value = '/machine'
        result = paths.inside_project(p)
        self.assertEqual(False, result)

    @mock.patch('projects.paths.os')
    def test__inside_project_root__returns_true(self, mock_os):
        p = '/machine/projects'
        mock_os.getcwd.return_value = '/machine/projects/project'
        result = paths.inside_project(p)
        self.assertEqual(True, result)

    @mock.patch('projects.paths.os')
    def test__deep_inside_project__returns_true(self, mock_os):
        p = '/machine/projects'
        mock_os.getcwd.return_value = '/machine/projects/project/d1/d2/d3'
        result = paths.inside_project(p)
        self.assertEqual(True, result)
