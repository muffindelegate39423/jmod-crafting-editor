from app.interface.ConfigOpener import *
from app.interface.MainWindow import *
import tkinter.messagebox
import configparser, os

setup_ini = os.path.join(os.path.dirname(__file__),"setup.ini")
language_dir = os.path.join(os.path.dirname(__file__),"lang/")
setup = configparser.ConfigParser()
lang = configparser.ConfigParser()

def read_setup_ini():
    if os.path.exists(setup_ini) == False:
        create_setup_ini()
    setup.read(setup_ini)
    setup_lang()

def create_setup_ini():
    setup["DEFAULT"] = {"language": "en_us",
                        "path": ""}
    setup.write(open(setup_ini,'w'))

def setup_lang():
    language = setup["DEFAULT"]["language"]
    language_path = language_dir+language+".txt"
    if os.path.exists(language_path) == True:
        lang.read(language_path)
    else:
        tkinter.messagebox.showerror(title="Missing language file",message=language_path+" is missing. Program will now close.")
        exit()

read_setup_ini()
opener = ConfigOpener(setup_ini,setup,lang)
opener.launch_reading_config()
gui = MainWindow(setup_ini,setup,lang)