import re


def _get_pattern(keys):
    ret = ''
    template = '[^{0}]*({0})'
    for key in keys:
        ret += template.format(key)
    return ret


class Filter(object):
    def __init__(self, data):
        self.lines = data
        self.keys = ''

    def add_key(self, key):
        self.keys += key
        pattern = re.compile(_get_pattern(self.keys))

        ret = []

        for line in self.lines:
            m = pattern.search(line)
            ret.append({
                'item': line,
                'selection': [
                    m.regs[1]
                ]
            })
        return ret




