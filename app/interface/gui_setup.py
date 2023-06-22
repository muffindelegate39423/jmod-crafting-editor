from tkinter import messagebox
from .widgets import *
from .config_opener import *
from .main_window import *
from os.path import exists

# class that setups the gui interface on program launch
class GuiSetup:
    def __init__(self,setup,setup_ini,lang_path,config_path):
        if exists(lang_path) == True: # if the language file exists, load it
            set_lang(lang_path)
        else: # otherwise, show an error message and close the program
            messagebox.showerror(title="Missing language file",
                                 message=lang_path+" is missing. Program will now close.")
            exit()
        set_setup(setup,setup_ini) # sets the setup data for widgets to use
        config_opener = ConfigOpener() # instantiate config opener
        config = config_opener.launch_config(config_path) # loads the config from setup.ini 
                                                          # as a dictionary
        if config != -1: # if a config has been opened
            set_jmod_dict(config) # sets the config for widgets to use
            MainWindow() # open main window
        else: # otherwise, close the program
            exit()