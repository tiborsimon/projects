import sys
from projects import config
from projects import paths

def main():
    print(sys.argv)
    try:
        conf = config.get()
        print(conf)
        if paths.inside_project(conf['projects-path']):
            print('Inside')
            pass
        else:
            print('Outside')
            pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
