import textwrap


def generate_doc(data, width):
    doc = '=' * width + '\n'
    name = data['name'].upper()
    name = '  '.join(name)
    name = name.center(width) + '\n'
    doc += name

    doc += '=' * width + '\n\n'
    if 'description' in data:
        doc += wrap_lines(data['description'], width, indent=1) + '\n\n'
    for command_name in data['commands']:
        command = data['commands'][command_name]
        if 'alias' in command:
            continue
        doc += command_name
        if 'alternatives' in command:
            doc += '|'
            doc += '|'.join(command['alternatives'])
        doc += ':'
        if 'dependencies' in command:
            doc += ' ['
            doc += ', '.join(command['dependencies'])
            doc += ']'
        doc += '\n\n'
        if 'description' in command:
            doc += wrap_lines(command['description'], width, indent=4)
        doc += '\n\n'
    return doc


def wrap_lines(raw, width, indent=0):
    ret = ''
    for p in [p.strip() for p in raw.split('\n') if p != '']:
        p_ret = ''
        wrapped = textwrap.wrap(p, width-4)
        for line in wrapped:
            p_ret += ' '*indent + line + '\n'
        ret += p_ret + '\n'
    return ret[:-1]


