from pyfiglet import Figlet


def generate_doc(data):
    f = Figlet(font='big')
    title = f.renderText(data['name'])
    return title + repr(data)
