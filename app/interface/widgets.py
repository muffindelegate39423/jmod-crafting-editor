from .PendingWindow import *
from ..lib import strmanip, arrayfuncs
from itertools import cycle
import tkinter, tkinter.messagebox
import configparser

class PathFrame:
    def __init__(self,parent,rowNum,columnNum,path):
        # path frame
        self.pathFrame = tkinter.Frame(parent,background="red")
        self.pathFrame.grid(row=rowNum,column=columnNum,columnspan=10,sticky="nesw")
        # path label
        self.pathLabel = tkinter.Label(self.pathFrame,text=strmanip.condense_path(path),font=("TkDefaultFont",8,"bold"))
        self.pathLabel.pack(padx=1,pady=1)

class CraftablesListFrame:
    def __init__(self,parent,rowNum,columnNum,craftablesDict,craftableNames,craftableEditColumn,l):
        # parent
        self.Parent = parent
        # lang
        self.lang = l
        # craftables dict
        self.craftables_dict = craftablesDict
        # craftable names
        self.craftable_names = craftableNames
        # craftable edit column
        self.craftable_edit_column = craftableEditColumn
        # list frame
        self.listFrame = tkinter.Frame(parent)
        self.listFrame.grid(row=rowNum,column=columnNum)
        # craftables listbox
        self.craftablesList = tkinter.Variable(value=self.craftable_names)
        self.craftablesListbox = tkinter.Listbox(self.listFrame,listvariable=self.craftablesList,selectmode="extended")
        self.craftablesListbox.pack(ipadx=45,ipady=130)
        # count label
        self.countTextVar = tkinter.StringVar()
        self.countLabel = tkinter.Label(self.listFrame,textvariable=self.countTextVar,font=("TkDefaultFont",10,"bold"))
        self.countLabel.pack()
        # selected label
        self.selectedTextVar = tkinter.StringVar()
        self.craftablesListbox.bind("<<ListboxSelect>>",lambda event:self.select())
        self.craftablesListbox.bind("<Delete>",lambda event:self.open_pending_window())
        self.selectedLabel = RainbowLabel(self.listFrame,self.selectedTextVar,"TkDefaultFont",10,"bold")
        # last selection
        self.lastSelection = ""
        # refresh widget contents
        self.refresh(self.craftable_names)

    def refresh(self,craftable_names):
        # update craftables listbox
        self.craftablesListbox.delete(0,"end")
        for c in self.craftable_names:
            self.craftablesListbox.insert("end",c)
        # update craftable count
        newText = self.lang["WIDGET"]["craftables"].format(count = str(len(craftable_names)))
        self.countTextVar.set(newText)
        # update selected count
        self.update_selected_text()

    def select(self):
        temp = self.craftablesListbox.curselection()
        if len(temp) > 0:
            curSelection = [temp[-1]]
            arrayfuncs.map_indexes(curSelection,self.craftable_names)
            curSelection = curSelection[-1]
            if curSelection != self.lastSelection:
                self.lastSelection = curSelection
                self.craftable_edit_column.load_info(self.lastSelection)
        self.update_selected_text()
    
    def update_selected_text(self):
        newText = ""
        count = len(self.craftablesListbox.curselection())
        if count > 0:
            newText = self.lang["WIDGET"]["selected"].format(count = str(count))
        self.selectedTextVar.set(newText)

    def open_pending_window(self):
        selected = list(self.craftablesListbox.curselection())
        count = len(selected)
        if count > 0:
            arrayfuncs.map_indexes(selected,self.craftable_names)
            pending_window = PendingWindow(self.Parent,self.lang,self.craftables_dict,selected,self.craftable_names,self.refresh)

class CraftableEditColumn:
    def __init__(self,parent,rowNum,columnNum,craftablesDict,l):
        # lang
        self.lang = l
        # craftables dict
        self.craftables_dict = craftablesDict
        # edit frame
        self.editFrame = tkinter.Frame(parent)
        self.editFrame.grid(row=rowNum,column=columnNum)
        # name label
        self.nameLabel = tkinter.Label(self.editFrame,text=self.lang["CRAFTABLE"]["name"]).grid(row=0,column=0,sticky="w")
        # name entry
        self.nameVar = tkinter.StringVar()
        self.nameEntry = tkinter.Entry(self.editFrame,textvariable=self.nameVar).grid(row=0,column=1,sticky="w")
        # size scale frame
        self.size_scale_frame = SizeScaleFrame(self.editFrame,1,0,self.lang)

    def load_info(self,craftableName):
        self.nameVar.set(craftableName)
        sizeScale = []
        craftingReqs = []
        results = []
        category = []
        craftingType = []
        description = []
        dictfuncs.get_craftable_data(self.craftables_dict,craftableName,sizeScale,craftingReqs,results,category,craftingType,description)
        #TO-DO

class SizeScaleFrame:
    def __init__(self,parent,rowNum,columnNum,l):
        # lang
        self.lang = l
        # size scale frame
        self.editFrame = tkinter.Frame(parent)
        self.editFrame.grid(row=rowNum,column=columnNum,columnspan=2,sticky="e")
        # scale check
        self.scaleCheck = tkinter.Checkbutton(self.editFrame,text=self.lang["CRAFTABLE"]["scale"]).grid(row=1,column=0,sticky="w")
        self.scaleSpinbox = tkinter.Spinbox(self.editFrame,from_=0,to=1000,width=3).grid(row=1,column=1,sticky="w")

    def load_size_scale(self,sizeScale):
        #TO-DO
        pass

class PendingListbox:
    def __init__(self,parent,rowNum,columnNum,selectedCraftables):
        # pending list
        self.pendingList = tkinter.Variable(value=selectedCraftables)
        # pending listbox
        self.pendingListbox = tkinter.Listbox(parent,listvariable=self.pendingList)
        self.pendingListbox.pack(fill="x",ipady=100)

class RainbowLabel:
    def __init__(self,parent,text,font,fontSize,fontProperty):
        self.rainbowFrame = tkinter.Frame(parent)
        self.rainbowFrame.pack()
        self.colors = cycle(strmanip.get_color_table())
        if type(text) == str:
            self.textVar = tkinter.StringVar()
            self.update_text(text)
        else:
            self.textVar = text
        self.rainbowLabel = tkinter.Label(self.rainbowFrame,textvariable=self.textVar,font=(font,fontSize,fontProperty))
        self.rainbowLabel.pack()
        self.update_color()
    
    def update_color(self):
        curColor = next(self.colors)
        self.rainbowLabel.config(fg=curColor)
        self.rainbowFrame.after(50,self.update_color)
    
    def update_text(self,textStr):
        self.textVar.set(textStr)