#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ProjectfileError(Exception):
    pass


PROJECTFILE_EMPTY_ERROR = 'Projectfile is empty! Or at least it does not contain any parsable text.'
PROJECTFILE_NO_COMMAND_ERROR = 'No commands were defined in the Projectfile!'
PROJECTFILE_NO_COMMAND_IN_COMMAND_ERROR = 'Command {} do not have any executable commands! Is this command necessary?'
PROJECTFILE_INVALID_DEPENDENCY = 'Invalid dependency "{}" for command "{}".'
PROJECTFILE_NO_PROJECTFILE = 'No Projectfile was found. Nothing to do..'
PROJECTFILE_ALTERNATIVE_REDEFINED = 'Alternative "{}" was used for both "{}" and "{}"..'

COMMENT_DELIMITER_UNEXPECTED_ERROR = 'Unexpected comment delimiter (""")!'
COMMAND_DELIMITER_UNEXPECTED_ERROR = 'Unexpected command delimiter (===)!'

VERSION_INDENTATION_ERROR = 'Whitespaces are not allowed before the "from" keyword!'
VERSION_FORMAT_ERROR = 'Invalid version format. The valid one looks like "v1.2.3".'
VERSION_MISSING_ERROR = 'You have to start your Projectfile with the minimum supported version!'

VARIABLE_INDENTATION_ERROR = 'Variables cannot be indented!'
VARIABLE_QUOTE_BEFORE_ERROR = 'No matching quote found at the beginning of value!'
VARIABLE_QUOTE_AFTER_ERROR = 'No matching quote found at the end of value!'
VARIABLE_SYNTAX_ERROR = 'Invalid variable format! It should be "my-variable = 42".'
VARIABLE_REDEFINED_ERROR = 'Variable "{}" was redefined in the Projectfile located in "{}". Original definition was located in "{}"!'

COMMAND_HEADER_INDENTATION_ERROR = 'Command header cannot be indented!'
COMMAND_HEADER_MISSING_COLON_ERROR = 'Missing colon after command name!'
COMMAND_HEADER_COLON_ERROR = 'Invalid colon placement! It should be "command:".'
COMMAND_HEADER_INVALID_ALTERNATIVE = 'Invalid command alternative syntax! It should be "command|c:".'
COMMAND_HEADER_EMPTY_DEPENDENCY_LIST = 'Empty dependency list!'
COMMAND_HEADER_INVALID_DEPENDENCY_LIST = 'Invalid dependency list syntax! It should be: "[dep1, dep2]".'
COMMAND_HEADER_SYNTAX_ERROR = 'Invalid command header format! It should be "command|c: [dep1, dep2]".'
COMMAND_HEADER_UNEXPECTED_UNINDENTED_ERROR = 'Unexpected unindented line!'
COMMAND_HEADER_REDEFINED_ERROR = 'Command "{}" was defined already!'
COMMAND_HEADER_PROHIBITED_COMMAND = 'Command "{}" is prohibited. Choose another name instead.'
