import urwid
from projects.filter import Filter

ll = [
    'projects',
    'matlab-library-system',
    'intervallum',
    'skillmath',
    'optimal-position',
    'site',
    'something',
    'regular-army-knife'
]

f = Filter(ll)


def generate_string(data):
    ret = []
    for item in data:

        for
        ret.append(item['string']+'\n')
    return ret


def exit_on_q(key):
    key = key.lower()
    if key in ('delete', 'backspace'):
        f.remove_key()
    else:
        f.add_key(key)
    fl = f.filter()
    s = generate_string(fl)
    txt.set_text(s)
    if key in ('esc',):
        raise urwid.ExitMainLoop()

palette = [
    ('text', 'light gray', 'black'),
    ('highlight', 'black', 'yellow'),
    ('bg', 'black', 'dark blue')]

txt = urwid.Text([('text', u"Hello World\n"), ('highlight', "Hello")], align='left')
map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1)
pad = urwid.Padding(fill, align='center', width=30)
loop = urwid.MainLoop(pad, palette, unhandled_input=exit_on_q)
loop.run()
