from app.interface.gui_setup import *
from configparser import ConfigParser
from os import path

# launch procedure
def main():
    # setup and language paths
    setup_ini = path.join(path.dirname(__file__),"setup.ini")
    lang_dir = path.join(path.dirname(__file__),"lang")
    setup = ConfigParser()
    lang = ConfigParser()
    # create setup.ini if it doesn't exist
    if path.exists(setup_ini) == False:
        create_setup_ini(setup,setup_ini)
    # load setup.ini
    setup.read(setup_ini,encoding='utf-8')
    # proceed to setting up the gui
    GuiSetup(setup=setup,
             setup_ini=setup_ini,
             lang_path=path.join(lang_dir,setup['DEFAULT']['lang']+".txt"),
             config_path=setup['DEFAULT']['path'])

# function that creates setup.ini
def create_setup_ini(setup,setup_ini):
    setup['DEFAULT'] = {'lang': 'en_us',
                        'path': '',
                        'updates': 'True'}
    setup.write(open(setup_ini,'w'))

# execute program
main()