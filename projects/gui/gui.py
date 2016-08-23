import pydoc

import urwid

from projects.gui import doc_generator
from projects.gui.project_selector import ProjectSelector


def select_project(project_list, path_callback):
    max_width = len(max(project_list, key=len))
    f = ProjectSelector(project_list, 'normal', 'highlighted', 'selected')

    def refresh_list(key=''):
        if key:
            if key in ('delete', 'backspace'):
                f.remove_key()
            else:
                if key in 'abcdefghijklmnopqrstuvwxyz- .0123456789':
                    f.add_key(key)
        s = f.render()
        txt.set_text(s)

    def exit_on_q(key):
        if key.__class__ is not str:
            return
        if key in ('Q',):
            raise urwid.ExitMainLoop()
        if key == 'up':
            f.up()
        if key == 'down':
            f.down()
        if key == 'enter':
            path_callback(f.select())
            raise urwid.ExitMainLoop()
        key = key.lower()
        refresh_list(key)

    palette = [
        ('normal', 'light gray', ''),
        ('selected', 'yellow, bold', ''),
        ('highlighted', 'black, bold', 'yellow'),
        ('quit button', 'light red, bold', ''),
        ('enter button', 'light green, bold', '')
    ]

    txt = urwid.Text('', align='left')
    fill = urwid.Filler(txt)
    pad = urwid.Padding(fill, align='center', width=max_width+4)
    box = urwid.LineBox(pad, title="Projects")

    footer = urwid.Text(['Start typing to search. Use arrow keys to navigate. Press (', ('enter button', 'Enter'), ') to select project. ', 'Press (', ('quit button', 'Q'), ') to exit.'])
    frame = urwid.Frame(body=box, footer=footer)

    loop = urwid.MainLoop(frame, palette, unhandled_input=exit_on_q)
    refresh_list()
    loop.run()


def show_project_details(data, width):
    doc = doc_generator.generate_doc(data, width)
    doc = doc.format(
        head='\033[0;33m',
        project='\033[1;36m',
        command='\033[1;33m',
        reset='\033[0m'
    )
    pydoc.pipepager(doc, cmd='less -R')
    # pydoc.pager(doc)

