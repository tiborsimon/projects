from subprocess import call
import os
from projects import config
from projects import paths
import gui


return_path = ''

def path_setting_callback(path):
    global return_path
    return_path = path


def main(args):
    try:
        conf = config.get()
        if paths.inside_project(conf['projects-path']):
            print('list commands')
        else:
            # start project selection
            gui.select_project(
                paths.list_dir_for_path(conf['projects-path']),
                path_setting_callback
            )
            if return_path:
                with open(os.path.join(os.path.expanduser('~'), '.p-path'), 'w+') as f:
                    f.write(os.path.join(os.path.expanduser(conf['projects-path']), return_path))

    except Exception as e:
        print(e)
        pass
