from ..lib import dictfuncs
from . import widgets
import tkinter
import json, configparser

class MainWindow:
    def __init__(self,ini,s,l):
        self.setup_ini = ini
        self.setup = s
        self.lang = l
        self.jmod_config_txt = self.setup["DEFAULT"]["path"]
        self.craftables = {}
        self.craftable_names = []
        self.known_craftingReqs = []
        self.known_categories = []
        self.known_craftingTypes = []
        self.load_data()
        self.display()

    def load_data(self):
        self.craftables = json.loads(open(self.jmod_config_txt,'r').read())["Craftables"]
        for c in self.craftables:
            self.craftable_names.append(c)
            dictfuncs.insert_from_2D_dict(self.craftables[c],self.known_craftingReqs,"craftingReqs")
            dictfuncs.insert_from_1D_dict(self.craftables[c],self.known_categories,"category")
            dictfuncs.insert_from_1D_dict(self.craftables[c],self.known_craftingTypes,"craftingType")
        self.known_craftingReqs.sort()
        self.known_categories.sort()
        self.known_craftingTypes.sort()

    def display(self):
        root = tkinter.Tk()
        root.title(self.lang["WINDOW"]["main"])
        root.geometry("566x634")
        root.resizable(0,0)
        path_frame = widgets.PathFrame(root,0,0,self.jmod_config_txt)
        craftables_list_frame = widgets.CraftablesListFrame(root,1,0,self.craftable_names)
        tkinter.mainloop()
