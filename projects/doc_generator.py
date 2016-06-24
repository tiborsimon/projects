from pyfiglet import Figlet




def generate_doc(data):
    f = Figlet(font='big')
    doc = f.renderText(data['name'])
    doc += '\n\n'
    if 'description' in data:
        doc += data['description'] + '\n\n\n'
    for command_name in data['commands']:
        command = data['commands'][command_name]
        if 'alias' in command:
            continue
        doc += command_name
        if 'alternatives' in command:
            doc += '|'
            doc += '|'.join(command['alternatives'])
            doc += '  '
        if 'dependencies' in command:
            doc += '['
            doc += ', '.join(command['dependecies'])
            doc += ']\n'
        doc += '\n\n'
        if 'description' in command:
            doc += command['description']

    return doc + repr(data)
