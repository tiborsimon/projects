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


class ProjectRootFinding(TestCase):
    def test__project_root_cen_be_calculated(self):
        projects_root = '/projects/root'
        current_path = '/projects/root/some-project'
        expected = {
            'path': '/projects/root/some-project',
            'name': 'some-project'
        }
        result = paths.get_project_root(projects_root, current_path)
        self.assertEqual(expected, result)

    def test__project_root_cen_be_calculated_deep_inside_the_project_too(self):
        projects_root = '/projects/root'
        current_path = '/projects/root/some-project/a/b/c/d/e/f/g/h/i'
        expected = {
            'path': '/projects/root/some-project',
            'name': 'some-project'
        }
        result = paths.get_project_root(projects_root, current_path)
        self.assertEqual(expected, result)


class ListDirForPath(TestCase):
    @mock.patch('projects.paths.os', autospec=True)
    def test__listing_with_hidden_folders(self, mock_os):
        mock_os.listdir.return_value = [
            '.hidden',
            'a',
            'b',
            'c'
        ]
        expected = [
            'a',
            'b',
            'c'
        ]
        result = paths.list_dir_for_path('my-path')
        self.assertEqual(expected, result)
        mock_os.path.expanduser.assert_called_with('my-path')


