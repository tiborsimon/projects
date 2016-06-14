import urwid
from projects.filter import Filter
from projects.gui import generate_gui_string


def select_project(project_list):
    f = Filter(project_list)
    context ={'current_index': 0}

    def refresh_list(key=''):
        search_content = search_text.text
        if key:
            if key in ('delete', 'backspace'):
                f.remove_key()
                if search_content:
                    search_content = search_content[:-1]
            else:
                if key in 'abcdefghijklmnopqrstuvwxyz- .':
                    f.add_key(key)
                    search_content += key
        fl = f.filter()
        s = generate_gui_string(fl, context['current_index'], 'text', 'highlight', 'index')
        txt.set_text(s)
        search_text.set_text(search_content)

    def exit_on_q(key):
        global current_index
        if key in ('Q',):
            raise urwid.ExitMainLoop()
        if key == 'up':
            if context['current_index'] > 0:
                context['current_index'] -= 1
        if key == 'down':
            if context['current_index'] < len(project_list)-1:
                context['current_index'] += 1
        key = key.lower()
        refresh_list(key)


    palette = [
        ('text', 'light gray', ''),
        ('search', 'black', 'white'),
        ('index', 'default,underline', ''),
        ('highlight', 'black', 'yellow'),
        ('quit button', 'dark red,bold', ''),
        ('bg', 'black', 'dark blue')]

    search_text = urwid.Text('')
    search = urwid.AttrMap(search_text, 'search')

    txt = urwid.Text([('text', 'a'), ('highlight', 'b'), ('text', 'c'), ('text', '\n')], align='left')
    txt_pad = urwid.Filler(txt, height='flow', top=1)
    pile = urwid.Pile([search, txt])
    fill = urwid.Filler(pile)
    pad = urwid.Padding(fill, align='center', width=18)
    box = urwid.LineBox(pad, title="Projects")

    footer = urwid.Text(['Start typing to search project. Use arrow keys to navigate. Press (Enter) to select project. ', 'Press (', ('quit button', 'Q'), ') to exit.'])
    # footer_box = urwid.LineBox(footer)
    frame = urwid.Frame(body=box, footer=footer)

    loop = urwid.MainLoop(frame, palette, unhandled_input=exit_on_q)
    refresh_list()
    loop.run()

if __name__ == '__main__':
    print('starting gui')
    l = [
        'imre',
        'bela',
        'gizike',
        'adorjan',
        'hello',
        'laskdjflkasj',
        'dkjfgiuenkjnc',
        'asdfarg',
        'asoiulsihf',
        'asdfhekrjher',
        'tseoijteo',
        'oeitjgoj',
        'oierjogijef',
        'oeisrofisf',
        'oeiroijiuhsdkj'
    ]
    select_project(l)
