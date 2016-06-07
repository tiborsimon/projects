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


class Filter(object):
    def __init__(self, data):
        self.lines = data
        self.keys = ''

    def generate_data_structure(self, key):
        self.keys += key
        pattern = re.compile(_get_pattern(self.keys))

        ret = []

        for line in self.lines:
            m = pattern.search(line)
            selection = m.regs[1:] if m else ()
            ret.append({
                'string': line,
                'selection': selection
            })
        return ret

    def add_key(self, key):
        data = self.generate_data_structure(key)
        sorted_data = self.sort_structure(data)
        return sorted_data

    def sort_structure(self, data):
        for item in data:
            weight_item(item)
        data = sorted(data, key=lambda k: k['weight'], reverse=True)
        for item in data:
            del item['weight']
        return data

