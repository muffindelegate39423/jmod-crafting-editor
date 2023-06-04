from lib import dictfuncs
import tkinter, tkinter.ttk, tkinter.filedialog
import json, os

path_ini = os.path.join(os.path.dirname(__file__),"path.ini")
jmod_config_txt = ""
craftables = {}
craftable_names = []
known_craftingReqs = []
known_categories = []
known_craftingTypes = []

def open_config():
    global jmod_config_txt
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
        craftable_names.append(c)
        dictfuncs.add_to_materials(craftables[c],known_craftingReqs,"craftingReqs")
        dictfuncs.add_to_keyList(craftables[c],known_categories,"category")
        dictfuncs.add_to_keyList(craftables[c],known_craftingTypes,"craftingType")
    known_craftingReqs.sort()
    known_categories.sort()
    known_craftingTypes.sort()

open_config()
load_data()

#WIP
root = tkinter.Tk()
root.title('JMod Crafting Editor')
root.geometry('566x634')
root.resizable(0,0)

pathFrame = tkinter.Frame(root,background="red")
pathFrame.grid(row=0,sticky="nesw")
pathLabel = tkinter.Label(pathFrame,text=jmod_config_txt,font=("TkDefaultFont",8,"bold"))
pathLabel.pack(fill="both",expand=True,padx=1,pady=1)

mainFrame = tkinter.Frame(root)
mainFrame.grid(row=1)

listFrame = tkinter.Frame(mainFrame)
listFrame.grid(column=0,row=0)
craftablesList = tkinter.Variable(value=craftable_names)
craftablesListbox = tkinter.Listbox(listFrame,listvariable=craftablesList,selectmode="extended")
craftablesListbox.pack(ipadx=45,ipady=130)
countLabel = tkinter.Label(listFrame,text=str(len(craftable_names))+" craftables",font=("TkDefaultFont",10,"bold"))
countLabel.pack()
selectedLabel = tkinter.Label(listFrame,text="0 selected",font=("TkDefaultFont",10,"bold"),fg="blue")
selectedLabel.pack()

editFrame = tkinter.Frame(mainFrame)
editFrame.grid(column=1,row=0,padx=5)
nameLabel = tkinter.Label(editFrame,text="Craftable Name: ").grid(row=0,column=0,sticky="w")
nameEntry = tkinter.Entry(editFrame).grid(column=1,row=0,sticky="w")
scaleRadio = tkinter.Checkbutton(editFrame,text="Size Scale").grid(row=2,column=0,sticky="w")
scaleSpinbox = tkinter.Spinbox(editFrame,from_=0,to=1000,width=3).grid(row=2,column=1,sticky="w")

editNotebook = tkinter.ttk.Notebook(editFrame)
editNotebook.grid(row=3,column=0,columnspan=2,sticky="w")
reqsFrame = tkinter.Frame(editNotebook,width=300,height=200)
reqsListbox = tkinter.Listbox(reqsFrame,height=12,width=37).grid(row=0,column=0)
reqsEditButton = tkinter.Button(reqsFrame,text="Edit").grid(row=1,column=0)
resultsFrame = tkinter.Frame(editNotebook,width=300,height=280)
resultsListbox = tkinter.Listbox(resultsFrame,height=12,width=37).grid(row=0,column=0)
resultsEditButton = tkinter.Button(resultsFrame,text="Edit").grid(row=1,column=0)
editNotebook.add(reqsFrame,text='Crafting Reqs')
editNotebook.add(resultsFrame,text='Results')

descriptionLabel = tkinter.Label(editFrame,text="Description",font=("TkDefaultFont",10,"underline")).grid(row=4,column=0,sticky="w")
descriptionText = tkinter.Text(editFrame,height=3,width=37,font=("TkDefaultFont")).grid(row=5,column=0,columnspan=2,sticky="w")
applyButton = tkinter.Button(editFrame,text="Apply Changes").grid(row=6,column=1,pady=10,sticky="e")

buttonFrame = tkinter.Frame(root)
buttonFrame["borderwidth"] = 1
buttonFrame["relief"] = "solid"
buttonFrame.grid(row=2)
openButton = tkinter.Button(buttonFrame,text="Open Config",width=20).grid(row=0,column=0)
saveButton = tkinter.Button(buttonFrame,text="Save Config",width=20).grid(row=0,column=1)
saveasButton = tkinter.Button(buttonFrame,text="Save Config As...",width=20).grid(row=0,column=2)
newButton = tkinter.Button(buttonFrame,text="New Craftable",width=20).grid(row=1,column=0)
sortButton = tkinter.Button(buttonFrame,text="Sort All Craftables",width=20).grid(row=1,column=1)
checkButton = tkinter.Button(buttonFrame,text="Check Broken Craftables",width=20).grid(row=1,column=2)
deleteButton = tkinter.Button(buttonFrame,text="Delete Craftable(s)",width=20).grid(row=2,column=0)
resetButton = tkinter.Button(buttonFrame,text="Reset Config",width=20).grid(row=2,column=1)
#WIP

tkinter.mainloop()