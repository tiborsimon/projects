import re


def _get_pattern(keys):
    ret = ''
    template = '[^{0}]*({0})'
    for key in keys:
        ret += template.format(key)
    return ret


def weight_item(item):
    item['weight'] = 0


class Filter(object):
    def __init__(self, data):
        self.lines = data
        self.keys = ''

    def generate_data_stucture(self, key):
        self.keys += key
        pattern = re.compile(_get_pattern(self.keys))

        ret = []

        for line in self.lines:
            m = pattern.search(line)
            selection = m.regs[1:] if m else ()
            ret.append({
                'line': line,
                'selection': selection
            })
        return ret

    def add_key(self, key):
        structure = self.generate_data_stucture(key)
        return structure
