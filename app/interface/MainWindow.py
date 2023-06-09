from . import widgets
from ..lib import dictfuncs
import tkinter
import json, configparser

class MainWindow:
    def __init__(self,ini,s,l):
        # setup.ini
        self.setup_ini = ini
        # setup
        self.setup = s
        # lang
        self.lang = l
        # jmod_config.txt
        self.jmod_config_txt = self.setup["DEFAULT"]["path"]
        # methods to call
        self.load_data()
        self.display()
    
    def load_data(self):
        # get craftables from jmod config file
        self.craftables_dict = dictfuncs.get_craftables(self.jmod_config_txt)
        # initialize lists
        self.craftable_names = []
        self.known_craftingReqs = []
        self.known_categories = []
        self.known_craftingTypes = []
        # get craftable properties
        dictfuncs.get_craftable_properties(self.craftables_dict,self.craftable_names,self.known_craftingReqs,self.known_categories,self.known_craftingTypes)
        # sort craftable properties
        self.known_craftingReqs.sort()
        self.known_categories.sort()
        self.known_craftingTypes.sort()
    
    def display(self):
        # window
        root = tkinter.Tk()
        root.title(self.lang["WINDOW"]["main"])
        root.geometry("566x634")
        root.resizable(0,0)
        # path frame
        path_frame = widgets.PathFrame(root,0,0,self.jmod_config_txt)
        # craftable edit column
        craftable_edit_column = widgets.CraftableEditColumn(root,1,1,self.craftables_dict,self.lang)
        # craftables list frame
        craftables_list_frame = widgets.CraftablesListFrame(root,1,0,self.craftables_dict,self.craftable_names,craftable_edit_column,self.lang)
        # mainloop
        tkinter.mainloop()
