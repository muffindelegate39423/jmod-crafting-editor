from lib import dictfuncs
import tkinter, tkinter.filedialog
import json, os

jmod_config_txt = ""
craftables = {}
known_craftingReqs = []
known_categories = []
known_craftingTypes = []

def open_config():
    global jmod_config_txt
    path_ini = os.path.join(os.path.dirname(__file__), "path.ini")
    try:
        jmod_config_txt = open(path_ini,'r').read()
    except:
        tkinter.messagebox.showwarning(title="Attention", message="temp")
        jmod_config_txt = tkinter.filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JMod config file", "*.txt"), ("All files", "*.*")]
        )
        if not jmod_config_txt:
            exit()
        else:
            open(path_ini,'w').write(jmod_config_txt)

def load_data():
    global craftables
    craftables = json.loads(open(jmod_config_txt,'r').read())["Craftables"]
    for c in craftables:
        dictfuncs.add_materials(craftables[c],known_craftingReqs,"craftingReqs")
        dictfuncs.add_to_keyList(craftables[c],known_categories,"category")
        dictfuncs.add_to_keyList(craftables[c],known_craftingTypes,"craftingType")
    known_craftingReqs.sort()
    known_categories.sort()
    known_craftingTypes.sort()

open_config()
load_data()
print(craftables)