#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    from unittest import mock

try:
    import __builtin__
    builtin_module = '__builtin__'
except ImportError:
    builtin_module = 'builtins'

from test.helpers import *

from projects.projectfile import error
from projects.projectfile.parser import state
from projects.projectfile import parser


class LinesProcessing(TestCase):
    def test__single_command_no_dependencies(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  echo "hello"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'pre': ['echo "hello"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_no_dependencies_more_commands(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  echo "hello"',
            '  cd ~',
            '  make html'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'pre': ['echo "hello"', 'cd ~', 'make html']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_with_dependencies(self):
        lines = [
            'from v1.2.3',
            '',
            'command: [a, b]',
            '  echo "hello"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'dependencies': ['a', 'b'],
                    'pre': ['echo "hello"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__more_commands_with_no_dependencies(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  echo "hello"',
            'command2:',
            '  echo "vmi"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'pre': ['echo "hello"']
                },
                'command2': {
                    'pre': ['echo "vmi"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_with_only_post(self):
        lines = [
            'from v1.2.3',
            '',
            'command: [a, b]',
            '  ===',
            '  echo "hello"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'dependencies': ['a', 'b'],
                    'post': ['echo "hello"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_with_pre_and_post(self):
        lines = [
            'from v1.2.3',
            '',
            'command: [a, b]',
            '  echo "pre"',
            '  ===',
            '  echo "post"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'dependencies': ['a', 'b'],
                    'post': ['echo "post"'],
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_with_variable(self):
        lines = [
            'from v1.2.3',
            '',
            'a = 42',
            'command: [a, b]',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'variables': {'a': '42'},
            'commands': {
                'command': {
                    'dependencies': ['a', 'b'],
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__single_command_with_variables(self):
        lines = [
            'from v1.2.3',
            '',
            'a = 42',
            'b = 54',
            'command: [a, b]',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'variables': {
                'a': '42',
                'b': '54'
            },
            'commands': {
                'command': {
                    'dependencies': ['a', 'b'],
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__main_comment(self):
        lines = [
            'from v1.2.3',
            '',
            '"""',
            'This is the main description',
            '"""',
            'command:',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is the main description',
            'commands': {
                'command': {
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__main_comment_indentation_gets_ignored(self):
        lines = [
            'from v1.2.3',
            '',
            '         """',
            '                This is the main description',
            '                  """',
            'command:',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is the main description',
            'commands': {
                'command': {
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__main_comment__inserting_line_break(self):
        lines = [
            'from v1.2.3',
            '',
            '"""',
            'This is the main description',
            '',
            'after break',
            '"""',
            'command:',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is the main description\n\nafter break',
            'commands': {
                'command': {
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__main_comment__appending_lines(self):
        lines = [
            'from v1.2.3',
            '',
            '"""',
            'This is the main description',
            'after break',
            '"""',
            'command:',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is the main description after break',
            'commands': {
                'command': {
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__command_comment(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  """',
            '  This is the command description',
            '  """',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'This is the command description',
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__command_comment_indentation_gets_ignored_1(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '"""',
            'This is the command description',
            '"""',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'This is the command description',
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__command_comment_indentation_gets_ignored_2(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '             """',
            '          This is the command description',
            '               """',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'This is the command description',
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__command_comment__inserting_line_break(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  """',
            '  This is the command description',
            '  ',
            '  vmi',
            '  """',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'This is the command description\n\nvmi',
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__command_comment__lines_appended_nicely(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '  """',
            '  This is the command description',
            '  vmi',
            '  """',
            '  echo "pre"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'commands': {
                'command': {
                    'description': 'This is the command description vmi',
                    'pre': ['echo "pre"']
                }
            }
        }
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__full_parsing(self):
        lines = [
            'from v1.2.3',
            '"""',
            'This is a test..',
            '"""',
            'a = 42',
            'b = 45',
            '',
            'command|com|c:',
            '  """',
            '  This is the command description.',
            '  vmi',
            '  """',
            '  echo "pre"',
            '  ===',
            '  echo "post"',
            '',
            'other_command|oth|oo|o: [command]',
            '  """',
            '  Another command..',
            '  """',
            '  echo "other"',
            '  echo "something"',
            '  ===',
            '  echo "post2"'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is a test..',
            'variables': {
                'a': '42',
                'b': '45'
            },
            'commands': {
                'command': {
                    'alternatives': ['com', 'c'],
                    'description': 'This is the command description. vmi',
                    'pre': ['echo "pre"'],
                    'post': ['echo "post"']
                },
                'com': {
                    'alias': 'command'
                },
                'c': {
                    'alias': 'command'
                },
                'other_command': {
                    'alternatives': ['oth', 'oo', 'o'],
                    'dependencies': ['command'],
                    'description': 'Another command..',
                    'pre': ['echo "other"', 'echo "something"'],
                    'post': ['echo "post2"']
                },
                'oth': {
                    'alias': 'other_command'
                },
                'oo': {
                    'alias': 'other_command'
                },
                'o': {
                    'alias': 'other_command'
                }
            }
        }
        self.maxDiff = None
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__full_parsing_with_comments_1(self):
        lines = [
            'from v1.2.3#comment',
            '"""#comment',
            'This is a test..#comment',
            '"""#comment',
            'a = 42#comment',
            'b = 45#comment',
            '#comment',
            'command|com|c:#comment',
            '  """#comment',
            '  This is the command description.#comment',
            '  vmi#comment',
            '  """#comment',
            '  echo "pre"#comment',
            '  ===#comment',
            '  echo "post"#comment',
            '#comment',
            'other_command|oth|oo|o: [command]#comment',
            '  """#comment',
            '  Another command..#comment',
            '  """#comment',
            '  echo "other"#comment',
            '  echo "something"#comment',
            '  ===#comment',
            '  echo "post2"#comment',
            '#comment'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is a test..#comment',
            'variables': {
                'a': '42',
                'b': '45'
            },
            'commands': {
                'command': {
                    'alternatives': ['com', 'c'],
                    'description': 'This is the command description.#comment vmi#comment',
                    'pre': ['echo "pre"'],
                    'post': ['echo "post"']
                },
                'com': {
                    'alias': 'command'
                },
                'c': {
                    'alias': 'command'
                },
                'other_command': {
                    'alternatives': ['oth', 'oo', 'o'],
                    'dependencies': ['command'],
                    'description': 'Another command..#comment',
                    'pre': ['echo "other"', 'echo "something"'],
                    'post': ['echo "post2"']
                },
                'oth': {
                    'alias': 'other_command'
                },
                'oo': {
                    'alias': 'other_command'
                },
                'o': {
                    'alias': 'other_command'
                }
            }
        }
        self.maxDiff = None
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)

    def test__full_parsing_with_comments_2(self):
        lines = [
            'from v1.2.3  #comment',
            '"""  #comment',
            'This is a test..  #comment',
            '"""  #comment',
            'a = 42  #comment',
            'b = 45  #comment',
            '  #comment',
            'command|com|c:  #comment',
            '  """  #comment',
            '  This is the command description.  #comment',
            '  vmi  #comment',
            '  """  #comment',
            '  echo "pre"  #comment',
            '  ===  #comment',
            '  echo "post"  #comment',
            '  #comment',
            'other_command|oth|oo|o: [command]  #comment',
            '  """  #comment',
            '  Another command..  #comment',
            '  """  #comment',
            '  echo "other"  #comment',
            '  echo "something"  #comment',
            '  ===  #comment',
            '  echo "post2"  #comment',
            '  #comment'
        ]
        expected = {
            'min-version': (1, 2, 3),
            'description': 'This is a test..  #comment',
            'variables': {
                'a': '42',
                'b': '45'
            },
            'commands': {
                'command': {
                    'alternatives': ['com', 'c'],
                    'description': 'This is the command description.  #comment vmi  #comment',
                    'pre': ['echo "pre"'],
                    'post': ['echo "post"']
                },
                'com': {
                    'alias': 'command'
                },
                'c': {
                    'alias': 'command'
                },
                'other_command': {
                    'alternatives': ['oth', 'oo', 'o'],
                    'dependencies': ['command'],
                    'description': 'Another command..  #comment',
                    'pre': ['echo "other"', 'echo "something"'],
                    'post': ['echo "post2"']
                },
                'oth': {
                    'alias': 'other_command'
                },
                'oo': {
                    'alias': 'other_command'
                },
                'o': {
                    'alias': 'other_command'
                }
            }
        }
        self.maxDiff = None
        result = parser._parse_lines(lines)
        self.assertEqual(expected, result)


class LineProcessingExceptionWrapping(TestCase):
    @mock.patch.object(state, 'start')
    def test__line_numbers_prepended_to_exception_message(self, mock_state):
        error_message = 'Some error'
        mock_state.side_effect = SyntaxError(error_message)
        expected_error = {
            'line': 1,
            'error': error_message
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines([''])
        assert_exception(self, cm, error.ProjectfileError, expected_error)


class ParserErrorCases(TestCase):
    def test__unexpected_comment_delimiter_1(self):
        lines = [
            'from v1.2.3',
            '',
            'a = 42',
            'b = 54',
            '"""'
        ]
        expected_error = {
            'line': 5,
            'error': error.COMMENT_DELIMITER_UNEXPECTED_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__unexpected_comment_delimiter_2(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '   cat file',
            '   """'
        ]
        expected_error = {
            'line': 5,
            'error': error.COMMENT_DELIMITER_UNEXPECTED_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__unexpected_comment_delimiter_3(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '   cat file',
            '   ===',
            '   cat file',
            '   """'
        ]
        expected_error = {
            'line': 7,
            'error': error.COMMENT_DELIMITER_UNEXPECTED_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__unexpected_command_delimiter(self):
        lines = [
            'from v1.2.3',
            '',
            'command:',
            '   cat file',
            '   ===',
            '   cat file',
            '   ==='
        ]
        expected_error = {
            'line': 7,
            'error': error.COMMAND_DELIMITER_UNEXPECTED_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__version_indentation_error(self):
        lines = [
            ' from v1.2.3'
        ]
        expected_error = {
            'line': 1,
            'error': error.VERSION_INDENTATION_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__invalid_version_format_error(self):
        lines = [
            'from v12.3'
        ]
        expected_error = {
            'line': 1,
            'error': error.VERSION_FORMAT_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__version_missing_error(self):
        lines = [
            'variable = 4'
        ]
        expected_error = {
            'line': 1,
            'error': error.VERSION_MISSING_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__variable_indentation_error(self):
        lines = [
            'from v1.2.3',
            '  variable = 4'
        ]
        expected_error = {
            'line': 2,
            'error': error.VARIABLE_INDENTATION_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__variable_quote_before_error(self):
        lines = [
            'from v1.2.3',
            'variable = 4"'
        ]
        expected_error = {
            'line': 2,
            'error': error.VARIABLE_QUOTE_BEFORE_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__variable_quote_after_error(self):
        lines = [
            'from v1.2.3',
            'variable = "4'
        ]
        expected_error = {
            'line': 2,
            'error': error.VARIABLE_QUOTE_AFTER_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test__variable_wrong_comment_placement(self):
        lines = [
            'from v1.2.3',
            'variable = #4'
        ]
        expected_error = {
            'line': 2,
            'error': error.VARIABLE_SYNTAX_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_header_indentation_error(self):
        lines = [
            'from v1.2.3',
            ' command:'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_INDENTATION_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_missing_colon_error(self):
        lines = [
            'from v1.2.3',
            'command'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_MISSING_COLON_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_invalid_colon_error(self):
        lines = [
            'from v1.2.3',
            'command:vmi'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_COLON_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_invalid_alternative_error(self):
        lines = [
            'from v1.2.3',
            'command|ffd|:'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_INVALID_ALTERNATIVE
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_empty_dependency_list_error(self):
        lines = [
            'from v1.2.3',
            'command: []'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_EMPTY_DEPENDENCY_LIST
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_invalid_dependency_list_error(self):
        lines = [
            'from v1.2.3',
            'command: [vmi,]'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_INVALID_DEPENDENCY_LIST
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_syntax_error(self):
        lines = [
            'from v1.2.3',
            'command: : [vmi,]'
        ]
        expected_error = {
            'line': 2,
            'error': error.COMMAND_HEADER_SYNTAX_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)

    def test_command_unexpected_unindented_line_error(self):
        lines = [
            'from v1.2.3',
            'command:',
            'vmi'
        ]
        expected_error = {
            'line': 3,
            'error': error.COMMAND_HEADER_UNEXPECTED_UNINDENTED_ERROR
        }
        with self.assertRaises(Exception) as cm:
            parser._parse_lines(lines)
        assert_exception(self, cm, error.ProjectfileError, expected_error)
