from .PendingWindow import *
from ..lib import strmanip, arrayfuncs
from itertools import cycle
import tkinter, tkinter.messagebox
import configparser

class PathFrame:
    def __init__(self,parent,rowNum,columnNum,path):
        # path frame
        self.pathFrame = tkinter.Frame(parent,background="red")
        self.pathFrame.grid(row=rowNum,column=columnNum,sticky="nesw")
        # path label
        self.pathLabel = tkinter.Label(self.pathFrame,text=strmanip.condense_path(path),font=("TkDefaultFont",8,"bold"))
        self.pathLabel.pack(padx=1,pady=1)

class CraftablesListFrame:
    def __init__(self,parent,rowNum,columnNum,craftableNames,l):
        # parent
        self.Parent = parent
        # lang
        self.lang = l
        # craftable names
        self.craftable_names = craftableNames
        # list frame
        self.listFrame = tkinter.Frame(parent)
        self.listFrame.grid(row=rowNum,column=columnNum)
        # craftables listbox
        self.craftablesList = tkinter.Variable(value=self.craftable_names)
        self.craftablesListbox = tkinter.Listbox(self.listFrame,listvariable=self.craftablesList,selectmode="extended")
        self.craftablesListbox.pack(ipadx=45,ipady=130)
        # count label
        self.countTextVar = tkinter.StringVar()
        self.update_count_text(self.craftable_names)
        self.countLabel = tkinter.Label(self.listFrame,textvariable=self.countTextVar,font=("TkDefaultFont",10,"bold"))
        self.countLabel.pack()
        # selected label
        self.selectedTextVar = tkinter.StringVar()
        self.craftablesListbox.bind("<<ListboxSelect>>", self.update_selected_text)
        self.craftablesListbox.bind("<Delete>", self.open_pending_window)
        self.selectedLabel = RainbowLabel(self.listFrame,self.selectedTextVar,"TkDefaultFont",10,"bold")
    
    def update_count_text(self,craftable_names):
        newText = self.lang["WIDGET"]["craftables"].format(count = str(len(craftable_names)))
        self.countTextVar.set(newText)

    def update_selected_text(self,event):
        newText = ""
        count = len(self.craftablesListbox.curselection())
        if count > 0:
            newText = self.lang["WIDGET"]["selected"].format(count = str(count))
        self.selectedTextVar.set(newText)

    def open_pending_window(self, event):
        selected = list(self.craftablesListbox.curselection())
        count = len(selected)
        if count > 0:
            arrayfuncs.map_indexes(selected,self.craftable_names)
            pending_window = PendingWindow(self.Parent,self.lang,selected)

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