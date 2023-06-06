from ..lib import strmanip
from itertools import cycle
import tkinter

class PathFrame:
    def __init__(self,parent,rowNum,columnNum,path):
        self.pathFrame = tkinter.Frame(parent,background="red")
        self.pathFrame.grid(row=rowNum,column=columnNum,sticky="nesw")
        self.pathLabel = tkinter.Label(self.pathFrame,text=strmanip.condense_path(path),font=("TkDefaultFont",8,"bold"))
        self.pathLabel.pack(padx=1,pady=1)

class CraftablesListFrame:
    def __init__(self,parent,rowNum,columnNum,craftableNames):
        self.listFrame = tkinter.Frame(parent)
        self.listFrame.grid(row=rowNum,column=columnNum)
        self.craftablesList = tkinter.Variable(value=craftableNames)
        self.craftablesListbox = tkinter.Listbox(self.listFrame,listvariable=self.craftablesList,selectmode="extended")
        self.craftablesListbox.pack(ipadx=45,ipady=130)
        self.countLabel = tkinter.Label(self.listFrame,text=str(len(craftableNames))+" craftables",font=("TkDefaultFont",10,"bold"))
        self.countLabel.pack()
        self.selectedLabel = RainbowLabel(self.listFrame,"0 selected","TkDefaultFont",10,"bold")

class RainbowLabel:
    def __init__(self,parent,textStr,font,fontSize,fontProperty):
        self.Parent = parent
        self.colors = cycle(strmanip.get_color_table())
        self.textVar = tkinter.StringVar()
        self.rainbowLabel = tkinter.Label(parent,textvariable=self.textVar,font=(font,fontSize,fontProperty))
        self.update_text(textStr)
        self.rainbowLabel.pack()
        self.update_color()

    def update_color(self):
        curColor = next(self.colors)
        self.rainbowLabel.config(fg=curColor)
        self.Parent.after(50,self.update_color)

    def update_text(self, textStr):
        self.textVar.set(textStr)
