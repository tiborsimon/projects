from projects import config
from projects import paths
import gui


def main(args):
    try:
        conf = config.get()
        if paths.inside_project(conf['projects-path']):
            print('ok')
            gui.start(paths.list_dir_for_path(conf['projects-path']))
        else:
            # start project selection
            gui.select_project(paths.list_dir_for_path(conf['projects-path']))
            pass

    except Exception as e:
        # print(e)
        pass
