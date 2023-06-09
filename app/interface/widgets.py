from .PendingWindow import *
from ..lib import strmanip, arrayfuncs
from itertools import cycle
import tkinter, tkinter.ttk, tkinter.messagebox
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
        # matching craftables (from search)
        self.matching_craftables = self.craftable_names
        # craftable edit column
        self.craftable_edit_column = craftableEditColumn
        # list frame
        self.listFrame = tkinter.Frame(parent)
        self.listFrame.grid(row=rowNum,column=columnNum)
        # craftables listbox (no pack)
        self.craftablesList = tkinter.Variable(value=self.craftable_names)
        self.craftablesListbox = tkinter.Listbox(self.listFrame,listvariable=self.craftablesList,selectmode="extended")
        # craftable searchbar
        self.craftable_searchbar = CraftableSearchbar(self.listFrame,self.lang["WIDGET"]["search"],self.craftable_names,self)
        # pack craftables listbox
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
        self.refresh()

    def refresh(self):
        # update craftables listbox
        self.update_matching_craftables(self.craftable_names)
        self.update_listbox(self.craftable_names)
        # update craftable count
        newText = self.lang["WIDGET"]["craftables"].format(count = str(len(self.craftable_names)))
        self.countTextVar.set(newText)
        # update selected count
        self.update_selected_text()

    def select(self):
        temp = self.craftablesListbox.curselection()
        if len(temp) > 0:
            curSelection = [temp[-1]]
            arrayfuncs.map_indexes(curSelection,self.matching_craftables)
            curSelection = curSelection[-1]
            if curSelection != self.lastSelection:
                self.lastSelection = curSelection
                self.craftable_edit_column.load_info(self.lastSelection)
        self.update_selected_text()

    def update_matching_craftables(self,newMatchlist):
        self.matching_craftables = newMatchlist

    def update_listbox(self,craftableNames):
        self.craftablesListbox.delete(0,"end")
        for c in craftableNames:
            self.craftablesListbox.insert("end",c)
    
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
            arrayfuncs.map_indexes(selected,self.matching_craftables)
            pending_window = PendingWindow(self.Parent,self.lang,self.craftables_dict,selected,self.craftable_names,self.refresh)

class CraftableSearchbar:
    def __init__(self,parent,defaultText,craftableNames,craftablesListbox):
        # default text
        self.default_text = defaultText
        # craftable names
        self.craftable_names = craftableNames
        # craftables listbox
        self.craftables_listbox = craftablesListbox
        # searchbar frame
        self.searchbarFrame = tkinter.Frame(parent)
        self.searchbarFrame.pack()
        # searchbar entry
        self.entryVar = tkinter.StringVar()
        self.searchbarEntry = tkinter.Entry(self.searchbarFrame,textvariable=self.entryVar,width=30,fg="gray")
        self.focus_out()
        self.searchbarEntry.pack()
        # searchbar binds
        self.searchbarEntry.bind("<FocusIn>",lambda event:self.focus_in())
        self.searchbarEntry.bind("<FocusOut>",lambda event:self.focus_out())
        self.searchbarEntry.bind('<KeyRelease>',lambda event:self.search())

    def focus_in(self):
        self.entryVar.set("")
        self.searchbarEntry.config(fg="black")
    
    def focus_out(self):
        curText = self.entryVar.get()
        if self.is_blank_space(curText) == True:
            self.entryVar.set(self.default_text)
            self.searchbarEntry.config(fg="gray")

    def search(self):
        curText = self.entryVar.get()
        if self.is_blank_space(curText) == False:
            matching_items = arrayfuncs.get_matching_items(curText,self.craftable_names)
            self.craftables_listbox.update_matching_craftables(matching_items)
            self.craftables_listbox.update_listbox(matching_items)
        else:
            self.craftables_listbox.refresh()

    def is_blank_space(self,string):
        if string == "\n" or string == "":
            return True
        else:
            return False

class CraftableEditColumn:
    def __init__(self,parent,rowNum,columnNum,craftablesDict,knownCategories,knownCraftingTypes,l):
        # lang
        self.lang = l
        # craftables dict
        self.craftables_dict = craftablesDict
        # edit frame
        self.editFrame = tkinter.Frame(parent)
        self.editFrame.grid(row=rowNum,column=columnNum)
        # name frame
        self.name_frame = FancyEntry(self.editFrame,0,0,self.lang["CRAFTABLE"]["name"])
        # size scale frame
        self.size_scale_frame = SizeScaleFrame(self.editFrame,1,0,self.lang)
        self.size_scale_frame.disable_spinbox()
        # category frame
        self.category_frame = FancyCombobox(self.editFrame,3,0,self.lang["CRAFTABLE"]["category"],knownCategories)
        # crafting type frame
        self.craftingType_frame = FancyCombobox(self.editFrame,4,0,self.lang["CRAFTABLE"]["crafting_type"],knownCraftingTypes)
        # results frame
        self.results_frame = FancyEntry(self.editFrame,5,0,self.lang["CRAFTABLE"]["results"])
        # description box
        self.description_box = DescriptionBox(self.editFrame,6,0,self.lang)

    def load_info(self,craftableName):
        self.name_frame.set_entry(craftableName)
        sizeScale = []
        craftingReqs = []
        results = []
        category = []
        craftingType = []
        description = []
        dictfuncs.get_craftable_data(self.craftables_dict,craftableName,sizeScale,craftingReqs,results,category,craftingType,description)
        if len(sizeScale) == 1:
            self.size_scale_frame.enable_spinbox()
            self.size_scale_frame.set_size_scale(sizeScale[0])
        else:
            self.size_scale_frame.disable_spinbox()
        if len(results) == 1:
            self.results_frame.set_entry(results[0])
        if len(category) == 1:
            self.category_frame.set_combobox(category[0])
        if len(craftingType) == 1:
            self.craftingType_frame.set_combobox(craftingType[0])
        if len(description) == 1:
            self.description_box.set_text(description[0])

class FancyEntry:
    def __init__(self,parent,rowNum,columnNum,labelStr):
        # fancy frame
        self.fancyFrame = tkinter.Frame(parent)
        self.fancyFrame.grid(row=rowNum,column=columnNum,sticky="w")
        # fancy label
        self.fancyLabel = tkinter.Label(self.fancyFrame,text=labelStr,font=("TkDefaultFont",10,"underline")).grid(row=0,column=0,sticky="w")
        # fancy entry
        self.entryVar = tkinter.StringVar()
        self.fancyEntry = tkinter.Entry(self.fancyFrame,textvariable=self.entryVar,width=25).grid(row=1,column=0,sticky="w")

    def set_entry(self,string):
        self.entryVar.set(string)
    
    def get_entry(self,string):
        self.entryVar.get(string)

class FancyCombobox:
    def __init__(self,parent,rowNum,columnNum,labelStr,optionsList):
        # fancy frame
        self.fancyFrame = tkinter.Frame(parent)
        self.fancyFrame.grid(row=rowNum,column=columnNum,sticky="w")
        # fancy label
        self.fancyLabel = tkinter.Label(self.fancyFrame,text=labelStr,font=("TkDefaultFont",10,"underline")).grid(row=0,column=0,sticky="w")
        # fancy combobox
        self.comboboxVar = tkinter.StringVar()
        self.fancyCombobox = tkinter.ttk.Combobox(self.fancyFrame,textvariable=self.comboboxVar,values=optionsList,width=25).grid(row=1,column=0,sticky="w")

    def set_combobox(self,string):
        self.comboboxVar.set(string)

    def get_combobox(self,string):
        self.comboboxVar.get(string)

class DescriptionBox:
    def __init__(self,parent,rowNum,columnNum,l):
        # lang
        self.lang = l
        # description frame
        self.descriptionFrame = tkinter.Frame(parent)
        self.descriptionFrame.grid(row=rowNum,column=columnNum,columnspan=2,sticky="w")
        # description label
        self.descriptionLabel = tkinter.Label(self.descriptionFrame,text=self.lang["CRAFTABLE"]["description"],font=("TkDefaultFont",10,"underline")).grid(row=0,column=0,sticky="w")
        # description text box
        self.descriptionText = tkinter.Text(self.descriptionFrame,height=5,width=25,font=("TkDefaultFont"))
        self.descriptionText.grid(row=1,column=0,columnspan=2,sticky="w")

    def set_text(self,string):
        self.clear_text()
        self.descriptionText.insert("1.0",string)
    
    def clear_text(self):
        self.descriptionText.delete("1.0","end")

    def get_text(self):
        text = self.descriptionText.get("1.0","end")
        return text

class SizeScaleFrame:
    def __init__(self,parent,rowNum,columnNum,l):
        # constants
        self.CHECKBOX_ONVALUE = "enable"
        self.CHECKBOX_OFFVALUE = "disable"
        self.SPINBOX_DEFAULTVALUE = 1.0
        self.SPINBOX_ROWNUM = 0
        self.SPINBOX_COLUMNNUM = 1
        # lang
        self.lang = l
        # size scale frame
        self.scaleFrame = tkinter.Frame(parent)
        self.scaleFrame.grid(row=rowNum,column=columnNum,columnspan=2,sticky="w")
        # scale checkbox
        self.checkboxVar = tkinter.StringVar()
        self.scaleCheckbox = tkinter.Checkbutton(self.scaleFrame,
                                                text=self.lang["CRAFTABLE"]["scale"],
                                                command=self.check_value,
                                                variable=self.checkboxVar,
                                                onvalue=self.CHECKBOX_ONVALUE,
                                                offvalue=self.CHECKBOX_OFFVALUE
                                                ).grid(row=0,column=0)
        # scale spinbox
        self.spinboxVar = tkinter.DoubleVar(value=self.SPINBOX_DEFAULTVALUE)
        self.scaleSpinbox = tkinter.Spinbox(self.scaleFrame,textvariable=self.spinboxVar,format="%.1f",increment=0.1,from_=0,to=100,width=4)
        self.scaleSpinbox.grid(row=self.SPINBOX_ROWNUM,column=self.SPINBOX_COLUMNNUM)

    def set_size_scale(self,sizeScale):
        self.spinboxVar.set(sizeScale)

    def is_checkbox_enabled(self):
        value = self.checkboxVar.get()
        if value == self.CHECKBOX_ONVALUE:
            return True
        else:
            return False

    def check_value(self):
        if self.is_checkbox_enabled() == True:
            self.enable_spinbox()
        else:
            self.disable_spinbox()

    def disable_spinbox(self):
        self.spinboxVar.set(self.SPINBOX_DEFAULTVALUE)
        self.checkboxVar.set(self.CHECKBOX_OFFVALUE)
        self.scaleSpinbox.grid_forget()

    def enable_spinbox(self):
        self.checkboxVar.set(self.CHECKBOX_ONVALUE)
        self.scaleSpinbox.grid(row=self.SPINBOX_ROWNUM,column=self.SPINBOX_COLUMNNUM)

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