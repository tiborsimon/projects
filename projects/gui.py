

def generate_gui_string(data, normal_palette, highlight_palette):
    ret = []
    for item in data:
        for piece in item:
            if piece['highlight']:
                a = (highlight_palette, piece['string'])
            else:
                a = (normal_palette, piece['string'])
            ret.append(a)
        ret.append((normal_palette, '\n'))
    return ret