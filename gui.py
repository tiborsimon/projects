import urwid
from projects.filter import Filter
from projects.gui import generate_gui_string


def select_project(project_list):
    f = Filter(project_list)

    def refresh_list():
        fl = f.filter()
        s = generate_gui_string(fl, 'text', 'highlight')
        txt.set_text(s)

    def exit_on_q(key):
        if key in ('Q',):
            raise urwid.ExitMainLoop()
        key = key.lower()
        if key in ('delete', 'backspace'):
            f.remove_key()
        else:
            f.add_key(key)
        refresh_list()


    palette = [
        ('text', 'light gray', 'black'),
        ('highlight', 'black', 'yellow'),
        ('bg', 'black', 'dark blue')]

    edit = urwid.Edit()
    txt = urwid.Text([('text', 'a'), ('highlight', 'b'), ('text', 'c'), ('text', '\n')], align='left')
    pile = urwid.Pile([edit, txt])
    fill = urwid.Filler(pile)

    refresh_list()
    pad = urwid.Padding(fill, align='center', width=30)
    box = urwid.LineBox(pad, title="Projects")
    loop = urwid.MainLoop(box, palette, unhandled_input=exit_on_q)
    loop.run()
