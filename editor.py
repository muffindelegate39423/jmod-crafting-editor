from lib import dictfuncs
import tkinter, tkinter.filedialog
import json, os

path_ini = os.path.join(os.path.dirname(__file__),"path.ini")
jmod_config_txt = ""
craftables = {}
known_craftingReqs = []
known_categories = []
known_craftingTypes = []

def open_config():
    global jmod_config_txt, path_ini
    try:
        jmod_config_txt = open(path_ini,'r').read()
        if dictfuncs.is_valid_config(jmod_config_txt) == False:
            tkinter.messagebox.showerror(title="Error",message="Config file cannot be read. Please select a valid config file.")
            set_config_path()
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="Attention",message="Please select a JMod config file.")
        set_config_path()

def set_config_path():
    global jmod_config_txt
    valid = False
    while valid == False:
        jmod_config_txt = tkinter.filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("JMod config file","*.txt"),("All files","*.*")]
        )
        if not jmod_config_txt:
            exit()
        else:
            if dictfuncs.is_valid_config(jmod_config_txt) == True:
                open(path_ini,'w').write(jmod_config_txt)
                valid = True
            else:
                tkinter.messagebox.showerror(title="Error",message="Invalid config file.")

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