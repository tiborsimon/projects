

def get_current_command(data):
    for command in data['commands']:
        if 'done' in data['commands'][command]:
            if not data['commands'][command]['done']:
                return data['commands'][command]
    else:
        return None
