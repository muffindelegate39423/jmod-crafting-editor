import json, configparser
from ..lib import dictfuncs

class MainWindow:
    jmod_config_txt = ""
    craftables = {}
    craftable_names = []
    known_craftingReqs = []
    known_categories = []
    known_craftingTypes = []

    setup_ini = ""
    setup = []
    lang = []

    def __init__(self,ini,s,l):
        self.setup_ini = ini
        self.setup = s
        self.lang = l
        self.jmod_config_txt = self.setup["DEFAULT"]["path"]
        self.load_data()

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