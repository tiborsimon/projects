import re


class ProjectSelector(object):
    def __init__(self, data, normal, highlighted, selected):
        self.data = data
        self.keys = ''
        self.focus = 0
        self.last_selection_result = _filter_data(self.keys, self.data)
        self.normal = normal
        self.highlighted = highlighted
        self.selected = selected

    def add_key(self, key):
        temp = self.keys
        temp += key
        result = _filter_data(temp, self.data)
        match_occurred = False
        for item in result:
            for part in item:
                if part['highlight']:
                    match_occurred = True
                    break
        if match_occurred:
            self.focus = 0
            self.last_selection_result = result
            self.keys = temp

    def remove_key(self):
        if len(self.keys) == 0:
            pass
        elif len(self.keys) == 1:
            self.keys = ''
        else:
            self.keys = self.keys[:-1]
        self.focus = 0
        self.last_selection_result = _filter_data(self.keys, self.data)

    def up(self):
        if self.focus > 0:
            self.focus -= 1

    def down(self):
        if self.focus < len(self.data)-1:
            self.focus += 1

    def select(self):
        ret = ''
        for part in self.last_selection_result[self.focus]:
            ret += part['string']
        return ret

    def render(self):
        return _render_string(
            self.last_selection_result,
            self.focus,
            self.normal,
            self.highlighted,
            self.selected
        )


def _get_pattern_list(keys):
    ret = []
    for i in reversed(range(1, len(keys)+1)):
        temp = ['']
        for j in range(len(keys)):
            if j < i:
                temp[0] += keys[j]
            else:
                temp.append('[^{}]*'.format(keys[j]))
                temp.append(keys[j])
        for k in range(len(temp)):
            if '^' not in temp[k]:
                temp[k] = '({})'.format(temp[k].replace('.', '\\.'))
        ret.append(''.join(temp))
    return ret


def _weight_for_item(item):
    return item['selection'][0][0]


def _weight_item(item):
    if item['selection']:
        item['weight'] = _weight_for_item(item)
    else:
        item['weight'] = 100000000000


def _sort_structure(data):
    _weight_it(data)
    data.sort(key=lambda k: k['string'])
    data.sort(key=lambda k: k['weight'])
    for item in data:
        del item['weight']
    return data


def _weight_it(data):
    for item in data:
        _weight_item(item)


def _merge_neighbour_selections(data):
    for node in data:
        merged = []
        last = ()
        if len(node['selection']) < 2:
            continue
        for s in node['selection']:
            if last:
                if last[1] == s[0]:
                    new_s = (last[0], s[1])
                    if merged:
                        merged.pop()
                    merged.append(new_s)
                    last = new_s
                else:
                    if not merged:
                        merged.append(last)
                    elif merged[-1] != last:
                        merged.append(last)
                    merged.append(s)
                    last = s
            else:
                last = s
        node['selection'] = tuple(merged)


def _generate_data_structure_for_search_string(patterns, search_string):
    ret = []
    for line in search_string:
        for pattern in patterns:
            p = re.compile(pattern)
            selections = []
            for m in p.finditer(line):
                selections.extend(m.regs[1:])
            if selections:
                ret.append({
                    'string': line,
                    'selection': tuple(selections)
                })
                break
        else:
            ret.append({
                'string': line,
                'selection': ()
            })
    _merge_neighbour_selections(ret)
    return ret


def _transform_data(data):
    ret = []
    for item in data:
        node = []
        if item['selection']:
            index = 0
            line = item['string']
            for s in item['selection']:
                if s[0] == 0:
                    node.append({
                        'string': line[:s[1]],
                        'highlight': True
                    })
                else:
                    node.append({
                        'string': line[index-index:s[0]-index],
                        'highlight': False
                    })
                    node.append({
                        'string': line[s[0]-index:s[1]-index],
                        'highlight': True
                    })
                line = line[s[1]-index:]
                index = s[1]

            else:
                if line:
                    node.append({
                        'string': line,
                        'highlight': False
                    })
        else:
            node.append({
                'string': item['string'],
                'highlight': False
            })
        ret.append(node)
    return ret


def _filter_data(keys, data):
    pattern = _get_pattern_list(keys)
    data = _generate_data_structure_for_search_string(pattern, data)
    sorted_data = _sort_structure(data)
    final_data = _transform_data(sorted_data)
    return final_data


def _render_string(data, index, normal, highlighted, selected):
    ret = []
    for i in range(len(data)):
        item = data[i]
        if i == index:
            ret.append((selected, '[ '))
        else:
            ret.append((normal, '  '))
        for piece in item:
            if piece['highlight']:
                a = (highlighted, piece['string'])
            else:
                a = (normal, piece['string'])
            ret.append(a)
        if i == index:
            ret.append((selected, ' ]'))
        ret.append((normal, '\n'))
    return ret



