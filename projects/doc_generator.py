from pyfiglet import Figlet


def generate_doc(data, pahts):
    f = Figlet(font='big')
    title = f.renderText('Projects')
    return title + '\nThe actual doc..'
