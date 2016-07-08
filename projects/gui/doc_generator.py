import textwrap


def generate_doc(data, width):
    doc = '=' * width + '\n'
    name = data['name'].upper()
    name = '  '.join(name)
    name = name.center(width).rstrip() + '\n'
    doc += name

    doc += '=' * width + '\n\n'
    if 'description' in data:
        doc += wrap_lines(data['description'], width, indent=1) + '\n\n'
    command_names = [cm for cm in data['commands']]
    for command_name in sorted(command_names):
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


def generate_markdown(data):
    ret = '# {}\n\n'.format(data['name'])
    if 'description' in data:
        ret += data['description'] + '\n\n'
    ret += '---\n\n'
    command_names = [cm for cm in data['commands']]
    for command_name in sorted(command_names):
        command = data['commands'][command_name]
        if 'alias' in command:
            continue
        ret += '### {}\n\n'.format(command_name)
        if 'alternatives' in command:
            alt = []
            for a in command['alternatives']:
                alt.append('`{}`'.format(a))
            ret += '- _alternatives_: {}\n'.format(', '.join(alt))
        if 'dependencies' in command:
            dep = []
            for d in command['dependencies']:
                dep.append('`{}`'.format(d))
            ret += '- _dependencies_: {}\n'.format(', '.join(dep))
        if 'description' in command:
            ret += '\n' + command['description'] + '\n\n'
    return ret
