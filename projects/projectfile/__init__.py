from . import data_processor

DEFAULT_PROJECTFILE = '''\
from v{}

"""
This is a template Projectfile you have created with the 'p [-i|--init]' command.
You can use the provided commands 'hello' and 'answer' or it's shorter alternatives
'h' and 'ans' or 'a'.

You can start a new paragraph in the descriptions by inserting an empty line like this.
"""

magic = 42

hello|h: [a]
    """
    This command will great you.
    """
    echo "This is the my very own Projectfile."

answer|ans|a:
    """
    This command will give you the answer for every question.
    """
    echo "The answer for everything is $magic!"
'''


def get_data_for_root(project_root):
    """This is the only API function of the projectfile module. It parses the Projectfiles
    from the given path and assembles the flattened command data structure.

    Returned data: {
        'min-version': (1, 0, 0),
        'description': 'Optional main description.',
        'commands': {
            'command_1': {
                'description': 'Optional command level description for command_1.',
                'script': [
                    'flattened',
                    'out command',
                    'list for',
                    'command_1',
                    ...
                ]
            }
            ...
        }
    }

    Raises:
        ProjectfileError with descriptive error message in the format of:
        {
            'path': 'Optional path for the corresponding Projectfile.',
            'line': 'Optional line number for the error in the Projectfile.',
            'error': 'Mandatory descriptive error message.'
        }


    :param project_root:
    :return: {dict} parsed and flattened commands with descriptions
    """
    processing_tree = data_processor.generate_processing_tree(project_root)
    data = data_processor.finalize_data(processing_tree)
    data_processor.process_variables(data)
    return data
