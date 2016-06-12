import urwid
from projects.filter import Filter
from projects.gui import generate_gui_string

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


def exit_on_q(key):
    key = key.lower()
    if key in ('delete', 'backspace'):
        f.remove_key()
    else:
        f.add_key(key)
    fl = f.filter()
    print(fl)
    s = generate_gui_string(fl, 'text', 'highlight')
    txt.set_text(s)
    if key in ('esc',):
        raise urwid.ExitMainLoop()

palette = [
    ('text', 'light gray', 'black'),
    ('highlight', 'black', 'yellow'),
    ('bg', 'black', 'dark blue')]

txt = urwid.Text([('text', 'a'), ('highlight', 'b'), ('text', 'c'), ('text', '\n')], align='left')
map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1)
pad = urwid.Padding(fill, align='center', width=30)
loop = urwid.MainLoop(pad, palette, unhandled_input=exit_on_q)
loop.run()
