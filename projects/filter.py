import re


def _get_pattern(keys):
    ret = ''
    template = '[^{0}]*({0})'
    for key in keys:
        ret += template.format(key)
    return ret


def weight_string_for_item(item):
    buffer = list('0'*len(item['string']))
    for s in item['selection']:
        for i in range(s[0], s[1]):
            buffer[i] = '1'
    return ''.join(buffer)


def weight_item(item):
    weight_string = weight_string_for_item(item)
    item['weight'] = int(weight_string, 2)


def sort_structure(data):
    for item in data:
        weight_item(item)
    data.sort(key=lambda k: k['string'])
    data.sort(key=lambda k: k['weight'], reverse=True)
    for item in data:
        del item['weight']
    return data


def generate_data_structure_for_search_string(pattern, search_string):
    p = re.compile(pattern)
    ret = []
    for line in search_string:
        m = p.search(line)
        selection = m.regs[1:] if m else ()
        ret.append({
            'string': line,
            'selection': selection
        })
    return ret


def filter_data(keys, data):
    pattern = _get_pattern(keys)
    data = generate_data_structure_for_search_string(pattern, data)
    sorted_data = sort_structure(data)
    return sorted_data


class Filter(object):
    def __init__(self, data):
        self.data = data
        self.keys = ''

    def add_key(self, key):
        self.keys += key

    def remove_key(self):
        if len(self.keys) == 0:
            pass
        elif len(self.keys) == 1:
            self.keys = ''
        else:
            self.keys = self.keys[:-1]

    def filter(self):
        return filter_data(self.keys, self.data)



