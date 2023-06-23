import tkinter as tk
from tkinter import ttk, messagebox
from .delete_window import *
from ..lib import dictfuncs, strmanip, arrayfuncs
from configparser import ConfigParser
from itertools import cycle
import webbrowser

_lang = []        # language data
_jmod_dict = []   # jmod dictionary
_setup = []       # setup data
_setup_ini = []   # setup.ini path

# function that sets the language data
# for this program from given path
def set_lang(path):
    global _lang
    _lang = ConfigParser()
    _lang.read(path)

# function that sets the jmod dictionary
# from current config file
def set_jmod_dict(jmod):
    _jmod_dict.clear()
    _jmod_dict.append(jmod)

# function that sets the setup data
# and the setup.ini path
def set_setup(setup,setup_ini):
    global _setup, _setup_ini
    _setup = setup
    _setup_ini = setup_ini

# function that saves the setup data
# to setup.ini
def save_setup():
    _setup.write(open(_setup_ini,'w'))

# widget with common data and operations
# inherited by most widgets in this program
class CommonWidget:
    def __init__(self,parent,row_num,column_num):
        # widget parent
        self.parent = parent
        # row number
        self.row_num = row_num
        # column number
        self.column_num = column_num
        # constant common width
        self.COMMON_WIDTH = 30
        # language data
        self.lang = _lang
        # jmod dictionary
        self.jmod_dict = _jmod_dict
        # setup data
        self.setup = _setup
    # returns common width that is
    # used for some widgets
    def get_common_width(self):
        return self.COMMON_WIDTH
    # returns language data
    def get_lang(self):
        return self.lang
    # returns jmod dictionary
    def get_jmod_dict(self):
        return self.jmod_dict[0]
    # returns widget's parent
    def get_parent(self):
        return self.parent
    # returns widget's row number in frame
    def get_row_num(self):
        return self.row_num
    # returns widget's column number in frame
    def get_column_num(self):
        return self.column_num
    # returns the config's jmod version
    def get_jmod_version(self):
        jmod = self.get_jmod_dict()
        jmod_version = dictfuncs.get_jmod_version(jmod)
        return jmod_version

# simple message box that shows an internal error message
# (used for debugging, not supposed to ever be seen!)
class InternalErrorMessage(CommonWidget):
    def __init__(self,cause):
        super().__init__(parent=None,row_num=None,column_num=None)
        messagebox.showerror(title=self.lang['MESSAGEBOX']['error'],
                             message=self.lang['DEBUG']['internal'].format(
                             newline='\n',
                             error=cause))

# common widget for entries
class EntryWidget(CommonWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        # entry string variable
        self.entry_var = tk.StringVar()
    # sets string entry
    def set_entry(self,string):
        self.entry_var.set(string)
    # returns string entry
    def get_entry(self):
        return self.entry_var.get()
    # clears entry
    def clear(self):
        self.entry_var.set("")
    # replaces existing string variable
    def set_entry_var(self,new_entry_var):
        self.entry_var = new_entry_var

# widget with label above entry field
class FancyEntry(EntryWidget):
    def __init__(self,parent,row_num,column_num,string):
        super().__init__(parent,row_num,column_num)
        # fancy frame
        self.fancy_frame = FrameWidget(parent)
        self.fancy_frame.grid(row=row_num,
                              column=column_num,
                              sticky='w')
        # fancy label
        self.fancy_label = tk.Label(self.fancy_frame,
                                    text=string,
                                    font=('TkDefaultFont',10,'underline'))
        self.fancy_label.grid(row=self.fancy_frame.get_available_row(),
                              column=0,sticky='w')
        # entry field is in inherited objects

# entrybox widget with label on top
class FancyEntryBox(FancyEntry):
    def __init__(self,parent,row_num,column_num,string):
        super().__init__(parent,row_num,column_num,string)
        # fancy entrybox
        self.fancy_entrybox = tk.Entry(self.fancy_frame,
                                       textvariable=self.entry_var,
                                       width=self.get_common_width())
        self.fancy_entrybox.grid(row=self.fancy_frame.get_available_row(),
                                 column=0,sticky='w')

# combobox widget with label on top
class FancyComboBox(FancyEntry):
    def __init__(self,parent,row_num,column_num,string):
        super().__init__(parent,row_num,column_num,string)
        self.boxlist = [] # list for combobox to use
        # fancy combobox
        self.fancy_combobox = ttk.Combobox(self.fancy_frame,
                                           textvariable=self.entry_var,
                                           values=self.boxlist,
                                           width=self.get_common_width())
        self.fancy_combobox.grid(row=1,column=0,sticky="w")
    # sets the boxlist
    def set_boxlist(self,boxlist):
        self.boxlist = boxlist
        self.fancy_combobox.config(values=self.boxlist)

# description box with label on top
class FancyDescriptionBox(FancyEntry):
    def __init__(self,parent,row_num,column_num,string):
        super().__init__(parent,row_num,column_num,string)
        # description text box
        self.fancy_descriptionbox = tk.Text(self.fancy_frame,
                                            height=5,
                                            width=self.get_common_width(),
                                            font=('TkDefaultFont'))
        self.fancy_descriptionbox.grid(row=self.fancy_frame.get_available_row(),
                                       column=0,sticky='w')
    # sets string entry
    def set_entry(self,string):
        self.clear()
        self.fancy_descriptionbox.insert('1.0',string)
    # returns string entry
    def get_entry(self):
        entry = self.fancy_descriptionbox.get('1.0','end').rstrip('\n')
        return entry
    # clears entry
    def clear(self):
        self.fancy_descriptionbox.delete('1.0','end')

# tk frame widget with additional operations
class FrameWidget(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
    # returns the "next available" column number
    def get_available_column(self):
        available_column = self.grid_size()[0]
        return available_column
    # returns the "next available" row number
    def get_available_row(self):
        available_row = self.grid_size()[1]
        return available_row

# label that opens a weblink when clicked on
class HyperlinkLabel(tk.Label):
    def __init__(self,parent,text,link):
        super().__init__(parent,
                         text=text,
                         font=('TkDefaultFont',10,'underline'),
                         fg='blue',cursor='hand2')
        self.bind('<Button-1>',lambda event:webbrowser.open_new_tab(link))

# searchbar widget for accompanying listbox
class ListboxSearchbar(EntryWidget):
    def __init__(self,parent,row_num,column_num,search_listbox,default_text):
        super().__init__(parent,row_num,column_num)
        # constant default text
        self.DEFAULT_TEXT = default_text
        # search listbox
        self.search_listbox = search_listbox
        # searchbar entry
        self.searchbar_entry = tk.Entry(parent,
                                        textvariable=self.entry_var,
                                        width=30)
        self.focus_out()
        self.searchbar_entry.grid(row=row_num,column=column_num)
        # searchbar binds
        self.searchbar_entry.bind("<FocusIn>",lambda event:self.focus_in())
        self.searchbar_entry.bind("<FocusOut>",lambda event:self.focus_out())
        self.searchbar_entry.bind("<KeyRelease>",lambda event:self.search())
    # displays input prompt
    def focus_in(self):
        self.clear()
        self.searchbar_entry.config(fg='black')
    # displays "focus out" prompt
    def focus_out(self):
        curText = self.entry_var.get()
        # if current text is empty
        if curText.isspace() == True or curText == "":
            # set the searchbar to show default text
            self.entry_var.set(self.DEFAULT_TEXT)
            self.searchbar_entry.config(fg='gray')
    # searches for matching items in listbox
    def search(self):
        curText = self.entry_var.get()
        # if current text doesn't have spaces
        if curText.isspace() == False:
            # get from and show matching items to listbox
            item_names = self.search_listbox.get_item_names()
            matching_items = arrayfuncs.get_matching_items(curText,item_names)
            self.search_listbox.set_displaying_items(matching_items)
        else: # otherwise, reset listbox contents to before search
            self.search_listbox.refresh()

# widget that displays craftable names
class SearchListbox(tk.Listbox):
    def __init__(self,parent,row_num,column_num,width,height):
        # listbox frame
        self.listbox_frame = FrameWidget(parent)
        self.listbox_frame.grid(row=row_num,column=column_num)
        # inherit tk listbox
        super().__init__(self.listbox_frame)
        # configure
        self.pack(side='left',ipadx=width,ipady=height)
        self.config(selectmode='extended')
        # listbox scrollbar
        self.scrollbar = ttk.Scrollbar(self.listbox_frame,
                                       orient='vertical',
                                       command=self.yview)
        self.scrollbar.pack(side='right',fill='y')
        self.configure(yscrollcommand=self.scrollbar.set)
        # listbox count variable
        self.count_var = tk.StringVar()
        self.count_format = ""
        # item names list
        self.item_names = []
    # sets item name data
    def set_item_names(self,items):
        self.item_names = items
        self.set_displaying_items(self.item_names)
    # sets list of items to be displayed
    def set_displaying_items(self,items):
        self.clear()
        for i in items:
            self.insert('end',i)
        self.update_item_count()
    # returns all item name data
    def get_item_names(self):
        return self.item_names
    # returns displaying items
    def get_list_items(self):
        return self.get(0,'end')
    # clears displaying items
    def clear(self):
        self.delete(0,'end')
        self.update_item_count()
    # refreshes displaying items
    # based on current item name data
    def refresh(self):
        self.set_displaying_items(self.item_names)
    # returns displaying item count variable
    def get_count_var(self):
        return self.count_var
    # sets the displaying item count string format
    def set_count_format(self,new_format):
        self.count_format = new_format
    # updates the displaying item count
    def update_item_count(self):
        temp = self.size()
        if self.count_format != "":
            temp = self.count_format.format(count=temp)
        self.count_var.set(temp)
    # removes multiple item name data
    def remove_item_names(self,items):
        for i in items:
            self.item_names.remove(i)
        self.refresh()
    # visually show item location inside listbox
    def show_item(self,item_name):
        index = self.item_names.index(item_name)
        self.selection_clear(0,'end')
        self.selection_set(index)
        self.see(index)

# widget that displays path of current config file
class PathDisplay(CommonWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        # path frame
        self.path_frame = FrameWidget(parent)
        self.path_frame.config(background='red')
        self.path_frame.grid(row=row_num,
                             column=column_num,
                             sticky='nesw')
        # path label text variable
        self.path_label_var = tk.StringVar()
        # path label
        self.path_label = tk.Label(self.path_frame,
                                   textvariable=self.path_label_var,
                                   font=('TkDefaultFont',8,'bold'))
        self.path_label.pack(fill='both',
                             expand=True,
                             padx=1,pady=1)
    # sets path from string parameter
    def set_path(self,path):
        temp = strmanip.condense_path(path)
        self.path_label_var.set(temp)

# popup entry widget for treeview
# (credit: @kurawlefaraaz for some code here)
class PopupEntry(EntryWidget):
    def __init__(self,parent,x,y,width,entry_value,boxlist):
        super().__init__(parent,row_num=None,column_num=None)
        # will the popup be a combobox?
        self.is_combobox = False
        # if no boxlist has been passed-through
        if boxlist == None:
            # popup will be a normal entrybox
            self.popup_entry = tk.Entry(parent)
        else: # otherwise, it will be a combobox
            self.popup_entry = ttk.Combobox(parent,
                                            values=boxlist)
            self.is_combobox = True
        # sets initial entry value to the popup
        self.entry_var.set(entry_value)
        # popup config
        self.popup_entry.config(justify='left',
                                textvariable=self.entry_var)
        self.popup_entry.place(x=x,y=y,width=width)
        self.popup_entry.focus_set()
        self.popup_entry.select_range(0,'end')
        # move cursor to the end
        self.popup_entry.icursor('end')
        # popup binds
        self.popup_entry.bind("<Return>",
                              lambda event:self.get_entry())
        if self.is_combobox == True:
            self.popup_entry.bind("<<ComboboxSelected>>",
                                  lambda event:self.get_entry())
        # wait
        self.wait_var = tk.StringVar(master=self.popup_entry)
        self.popup_entry.wait_window()
    # returns popup entry
    def get_entry(self):
        temp = self.entry_var.get()
        if self.is_combobox == False:
            temp = self.format_num_entry(temp)
        self.popup_entry.destroy()
        return temp
    # formats numerical entry to be decimal
    def format_num_entry(self,numEntry):
        temp = numEntry.replace('.','')
        if temp.isdigit() == False or int(temp) <= 0:
            numEntry = "0.0"
        else:
            numEntry = "{:.1f}".format(float(numEntry))
        return numEntry

# crafting req edit tree widget
# (credit: @kurawlefaraaz for some code here)
class ReqEditTree(CommonWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        # crafting reqs boxlist
        self.crafting_reqs_list = []
        # req edit frame
        self.req_edit_frame = FrameWidget(parent)
        self.req_edit_frame.grid(row=row_num,column=column_num,sticky='w')
        # req label
        self.req_label = tk.Label(self.req_edit_frame,
                                  text=self.lang['CRAFTABLE']['crafting_reqs'],
                                  font=('TkDefaultFont',10,'underline'))
        self.req_label.grid(row=self.req_edit_frame.get_available_row(),
                            column=0,sticky='w')
        # req edit tree
        self.req_edit_tree = ttk.Treeview(self.req_edit_frame,
                                          column=('c1','c2'),
                                          show='headings',height=8)
        self.req_edit_tree.grid(row=self.req_edit_frame.get_available_row(),
                                column=0)
        self.req_edit_tree.column('#1',anchor='w',width=135)
        self.req_edit_tree.heading('#1',text=self.lang['WIDGET']['material'])
        self.req_edit_tree.column('#2',anchor='w',width=69)
        self.req_edit_tree.heading('#2',text=self.lang['WIDGET']['amount'])
        # button frame
        self.button_frame = FrameWidget(self.req_edit_frame)
        self.button_frame.grid(row=self.req_edit_frame.get_available_row(),
                               column=0)
        # new button
        self.new_button = tk.Button(self.button_frame,
                                   text=self.lang['MATERIAL']['new'],
                                   command=self.add_new_material)
        self.new_button.grid(row=0,
                            column=self.button_frame.get_available_column())
        # edit button
        self.edit_button = tk.Button(self.button_frame,
                                    text=self.lang['MATERIAL']['edit'],
                                    command=lambda:self.edit_material(double_clicked=False))
        self.edit_button.grid(row=0,column=self.button_frame.get_available_column())
        # delete button
        self.delete_button = tk.Button(self.button_frame,text=self.lang['MATERIAL']['delete'],
                                      command=self.delete_material)
        self.delete_button.grid(row=0,column=self.button_frame.get_available_column())
        # item iid
        self.iid = 0
        # req edit tree binds
        self.req_edit_tree.bind("<Delete>",lambda event:self.delete_material())
        self.req_edit_tree.bind('<Double Button-1>',
                                lambda event:self.edit_material(double_clicked=True))
    # creates and adds new material to tree
    def add_new_material(self):
        self.insert_material(self.lang['MATERIAL']['new_material'],0.0)
    # clears entry
    def clear(self):
        for t in self.req_edit_tree.get_children():
            self.req_edit_tree.delete(t)
        self.iid = 0 # reset tree iids
    # removes material from tree
    def delete_material(self):
        try:
            current_material = self.req_edit_tree.selection()[0]
            self.req_edit_tree.delete(current_material)
        except IndexError:
            pass
    # edits selected material in tree
    def edit_material(self,double_clicked):
        try:
            # selected material
            current_row = self.req_edit_tree.focus()
            # index of current row
            current_index = self.req_edit_tree.index(current_row)
            # row and column values
            current_row_values = list(self.req_edit_tree.item(current_row,'values'))
            current_row_num = self.get_current_row_num()
            current_column_num = self.get_current_column_num()
            # selected cell value
            current_cell_value = current_row_values[current_column_num]
            # if there are values
            if len(current_row_values) != 0:
                # if a tree cell has been double clicked on
                if double_clicked == True and self.is_cell() == True:
                    # calculate popup entry placement
                    entry_placement = self.req_edit_tree.bbox(current_row,
                                                              column=current_column_num)
                    # check if current column is for numeral input (needs an entrybox)
                    if current_column_num == 1:
                        box_list = None
                    else: # if not, then it's string-based and needs a boxlist
                        box_list = self.crafting_reqs_list
                    # instantiate popup entry
                    popup_entry = PopupEntry(self.req_edit_tree,
                                             x=entry_placement[0],
                                             y=entry_placement[1],
                                             width=entry_placement[2],
                                             entry_value=current_cell_value,
                                             boxlist=box_list)
                    # after popup entry has been destroyed
                    new_cell_value = popup_entry.get_entry()
                    # update cell value
                    current_row_values[current_column_num] = new_cell_value
                    # update row
                    self.update_row(values=current_row_values,
                                    curRow=current_row,
                                    curIndex=current_index)
                # otherwise... (if the tree cell wasn't double clicked on)
                # traverse edit through the row
                elif double_clicked == False:
                    # left popup will appear
                    left_entry_placement = self.req_edit_tree.bbox(current_row,column=0)
                    current_cell_value = current_row_values[0]
                    popup_entry = PopupEntry(self.req_edit_tree,
                                             x=left_entry_placement[0],
                                             y=left_entry_placement[1],
                                             width=left_entry_placement[2],
                                             entry_value=current_cell_value,
                                             boxlist=self.crafting_reqs_list)
                    current_row_values[0] = popup_entry.get_entry()
                    self.update_row(values=current_row_values,curRow=current_row,curIndex=current_index)
                    # right popup will appear
                    right_entry_placement = self.req_edit_tree.bbox(current_row,column=1)
                    current_cell_value = current_row_values[1]
                    popup_entry = PopupEntry(self.req_edit_tree,
                                             x=right_entry_placement[0],
                                             y=right_entry_placement[1],
                                             width=right_entry_placement[2],
                                             entry_value=current_cell_value,
                                             boxlist=None)
                    current_row_values[1] = popup_entry.get_entry()
                    self.update_row(values=current_row_values,curRow=current_row,curIndex=current_index)
        except IndexError:
            pass
    # returns current row number
    def get_current_row_num(self):
        current_row_num = self.req_edit_tree.index(self.req_edit_tree.selection())+1
        return current_row_num
    # returns current column number
    def get_current_column_num(self):
        root_x = self.req_edit_tree.winfo_pointerx()
        widget_x = self.req_edit_tree.winfo_rootx()
        x = root_x - widget_x
        current_column_num = int(self.req_edit_tree.identify_column(x).replace('#',''))-1
        return current_column_num
    # returns tree entry
    def get_entry(self):
        temp = {} # entry is dictionary to store all materials and values of the craftable
        for t in self.req_edit_tree.get_children():
            material_data = self.req_edit_tree.item(t,'values')
            curMaterial = material_data[0] # material name
            curAmount = material_data[1] # material quantity
            # if the current material is not a duplicate
            if curMaterial not in temp:
                temp[curMaterial] = curAmount
            else: # otherwise, add all of its amounts
                temp[curMaterial] = "{:.1f}".format(float(temp[curMaterial])+float(curAmount))
            temp[curMaterial] = float(temp[curMaterial]) # type-cast the amount to float
        self.set_entry(temp) # update the material in tree also
        return temp
    # returns a new item iid
    def get_new_iid(self):
        new_iid = self.iid
        self.iid += 1
        return new_iid
    # inserts material to tree
    # (different from adding new material)
    def insert_material(self,material,amount):
        self.req_edit_tree.insert('','end',self.get_new_iid(),values=(material,amount))
    # is the selected tree region a cell?
    def is_cell(self):
        temp = self.req_edit_tree.identify_region(x=(self.req_edit_tree.winfo_pointerx()-self.req_edit_tree.winfo_rootx()),
                                                  y=(self.req_edit_tree.winfo_pointery()-self.req_edit_tree.winfo_rooty()))
        if temp == "cell":
            return True
        else:
            return False
    # sets crafting reqs boxlist
    def set_boxlist(self,boxlist):
        self.crafting_reqs_list = boxlist
    # sets tree entry
    def set_entry(self,materials):
        self.clear()
        for m,a in materials.items():
            self.insert_material(m,a)
    # updates current row
    def update_row(self,values,curRow,curIndex):
        try:
            self.req_edit_tree.delete(curRow)
            # put the row back in with the updated values
            self.req_edit_tree.insert('',curIndex,curRow,values=values)
        except tk.TclError:
            pass
    
# colorful rainbow label widget
class RainbowLabel:
    def __init__(self,parent,row_num,column_num,string,font,font_size,font_property):
        # rainbow frame
        self.rainbow_frame = tk.Frame(parent)
        self.rainbow_frame.grid(row=row_num,column=column_num)
        # rainbow colors
        self.colors = cycle(strmanip.get_color_table())
        # if label string really is a string...
        if type(string) == str:
            # it gets set TO a tk variable
            self.text_var = tk.StringVar()
            self.set_text(string)
        # otherwise...
        else:
            # it gets set AS a tk variable
            self.text_var = string
        # rainbow label
        self.rainbow_label = tk.Label(self.rainbow_frame,
                                      textvariable=self.text_var,
                                      font=(font,font_size,font_property))
        self.rainbow_label.pack()
        # update color loop
        self.__update_color()
    # constantly updates label color
    def __update_color(self):
        curColor = next(self.colors)
        self.rainbow_label.config(fg=curColor)
        self.rainbow_frame.after(50,self.__update_color)
    # sets label text
    def set_text(self,textStr):
        self.text_var.set(textStr)
    # returns label text
    def get_text(self):
        return self.text_var.get()

# widget that displays the number of selected listbox items
# and stores those items
class SelectionDisplay(CommonWidget):
    def __init__(self,parent,row_num,column_num,string):
        super().__init__(parent,row_num,column_num)
        # selected label
        self.selected_var = tk.StringVar()
        self.selected_label = RainbowLabel(parent,
                                           row_num=parent.get_available_row(),
                                           column_num=0,
                                           string=self.selected_var,
                                           font='TkDefaultFont',
                                           font_size=10,
                                           font_property='bold')
        self.selected_format = string
        # selected items list
        self.selected_items = []
    # updates selected items count
    def update(self,selection):
        # set selected itmes
        self.selected_items = selection
        # display selected count
        num = len(self.selected_items)
        temp = ""
        # if the count is greater than 0
        if num > 0:
            # display the counter
            temp = self.selected_format.format(count=num)
        self.selected_var.set(temp)
    # returns the list of selected items
    def get_selected_items(self):
        return self.selected_items
    # clears the selected items list and
    # counter
    def clear(self):
        self.selected_items.clear()
        self.selected_var.set("")

# toggleable spinbox entry that sets the
# size scale of a craftable
class SizeScaleEntry(EntryWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        # constant checkbox values
        self.CHECKBOX_ONVALUE = "enable"
        self.CHECKBOX_OFFVALUE = "disable"
        # constant spinbox values
        self.SPINBOX_DEFAULTVALUE = "1.0"
        self.SPINBOX_FROMVALUE = 0
        self.SPINBOX_TOVALUE = 100
        # size scale frame
        self.scale_frame = FrameWidget(parent)
        self.scale_frame.grid(row=row_num,column=column_num,sticky='w')
        # size scale checkbox
        self.checkbox_var = tk.StringVar()
        self.scale_checkbox = tk.Checkbutton(self.scale_frame,
                                             text=self.lang['CRAFTABLE']['scale'],
                                             command=self.check_value,
                                             variable=self.checkbox_var,
                                             onvalue=self.CHECKBOX_ONVALUE,
                                             offvalue=self.CHECKBOX_OFFVALUE)
        self.scale_checkbox.grid(row=0,column=0)
        # size scale spinbox
        self.spinbox_var = tk.DoubleVar(value=self.SPINBOX_DEFAULTVALUE)
        self.scale_spinbox = tk.Spinbox(self.scale_frame,
                                        textvariable=self.spinbox_var,
                                        width=4,
                                        format="%.1f",
                                        increment=0.1,
                                        from_=self.SPINBOX_FROMVALUE,
                                        to=self.SPINBOX_TOVALUE)
        self.scale_spinbox.grid(row=0,
                                column=self.scale_frame.get_available_column())
        # replaces inherited entry string variable
        self.set_entry_var(self.spinbox_var)
    # enables/disables spinbox based on
    # checkbox value
    def check_value(self):
        if self.is_checkbox_enabled() == True:
            self.enable_spinbox()
        else:
            self.disable_spinbox()
    # enables (shows) spinbox
    def enable_spinbox(self):
        self.checkbox_var.set(self.CHECKBOX_ONVALUE)
        self.scale_spinbox.grid(row=0,
                                column=self.scale_frame.get_available_column())
    # disables (hides) spinbox
    def disable_spinbox(self):
        self.spinbox_var.set(self.SPINBOX_DEFAULTVALUE)
        self.checkbox_var.set(self.CHECKBOX_OFFVALUE)
        self.scale_spinbox.grid_forget()
    # is checkbox currently enabled?
    def is_checkbox_enabled(self):
        temp = self.checkbox_var.get()
        if temp == self.CHECKBOX_ONVALUE:
            return True
        else:
            return False
    # sets string entry
    def set_entry(self,scale):
        self.spinbox_var.set(scale)

# widget that contains the craftables listbox and searchbar
class CraftablesListFrame(CommonWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        self.craftables_edit_frame = [] # preload edit frame
        # internal list frame
        self.craftables_list_frame = FrameWidget(parent)
        self.craftables_list_frame.grid(row=row_num,column=column_num,padx=25)
        # listbox
        self.craftables_listbox = SearchListbox(self.craftables_list_frame,
                                                row_num=1,column_num=0,
                                                width=45,height=164)
        # searchbar (requires listbox above)
        self.craftables_searchbar = ListboxSearchbar(self.craftables_list_frame,
                                                     row_num=0,column_num=0,
                                                     search_listbox=self.craftables_listbox,
                                                     default_text=self.lang['WIDGET']['search'])
        # craftables count label
        self.count_var = self.craftables_listbox.get_count_var()
        self.count_label = tk.Label(self.craftables_list_frame,
                                    textvariable=self.count_var,
                                    font=('TkDefaultFont',10,'bold'))
        self.count_label.grid(row=self.craftables_list_frame.get_available_row(),column=0)
        # set listbox count format
        self.craftables_listbox.set_count_format(self.lang['WIDGET']['craftables'])
        # update listbox item count for first time
        self.craftables_listbox.update_item_count()
        # craftables selected label
        self.selected_label = SelectionDisplay(self.craftables_list_frame,
                                               row_num=self.craftables_list_frame.get_available_row(),
                                               column_num=0,string=self.lang['WIDGET']['selected'])
        # craftables list binds
        self.craftables_listbox.bind("<<ListboxSelect>>",lambda event:self.select_craftable())
        self.craftables_listbox.bind("<Delete>",lambda event:self.open_delete_window())
    # sets edit frame needed when selecting a craftable
    def set_edit_frame(self,edit_frame):
        self.craftables_edit_frame = edit_frame
    # sets craftable names inside listbox
    def set_craftables(self,craftables):
        self.craftables_listbox.set_item_names(craftables)
    # loads currently selected craftable data in the edit frame
    def select_craftable(self):
        selection = list(self.craftables_listbox.curselection())
        arrayfuncs.map_indexes(selection,self.craftables_listbox.get_list_items())
        self.selected_label.update(selection)
        try:
            self.craftables_edit_frame.load_data(selection[-1])
        except IndexError:
            pass
        except AttributeError:
            InternalErrorMessage("Edit frame not binded OR missing dictfunc")
    # opens delete window 
    # (requires at least 1 selected craftable to open)
    def open_delete_window(self):
        selection_count = len(self.craftables_listbox.curselection())
        if selection_count > 0:
            selected_craftables = self.selected_label.get_selected_items()
            delete_window = DeleteWindow(CommonWidget,FrameWidget,
                                         listbox=self.craftables_listbox,
                                         selected_items=selected_craftables,
                                         selected_label=self.selected_label)
    # reloads craftable names inside listbox
    def reload_craftables(self):
        temp = self.get_jmod_dict()
        craftable_names = dictfuncs.get_craftable_names(temp,self.get_jmod_version())
        self.set_craftables(craftable_names)
    # shows item location inside listbox
    def show_item(self,item_name):
        self.reload_craftables()
        self.craftables_listbox.show_item(item_name)
        self.select_craftable()
    # clears listbox selection
    def clear_selection(self):
        self.craftables_listbox.clear()
        self.selected_label.clear()

# widget that allows the user to edit selected craftable data
class CraftablesEditFrame(CommonWidget):
    def __init__(self,parent,row_num,column_num):
        super().__init__(parent,row_num,column_num)
        self.craftables_list_frame = [] # preload list frame
        # original craftable name upon selection
        self.craftable_name = ""
        # known crafting reqs list
        self.crafting_reqs_list = []
        # known categories list
        self.categories_list = []
        # known crafting types list
        self.crafting_types_list = []
        # craftable edit frame
        self.craftables_edit_frame = FrameWidget(self.get_parent())
        self.craftables_edit_frame.grid(row=self.get_row_num(),
                                        column=self.get_column_num(),padx=25)
        # craftable name entry
        self.name_entry = FancyEntryBox(self.craftables_edit_frame,
                                        row_num=self.craftables_edit_frame.get_available_row(),
                                        column_num=0,
                                        string=self.lang['CRAFTABLE']['name'])
        # size scale entry
        self.scale_entry = SizeScaleEntry(self.craftables_edit_frame,
                                          row_num=self.craftables_edit_frame.get_available_row(),
                                          column_num=0)
        self.scale_entry.disable_spinbox() # spinbox is disabled by default
        # crafting reqs tree
        self.crafting_reqs_tree = ReqEditTree(self.craftables_edit_frame,
                                              row_num=self.craftables_edit_frame.get_available_row(),
                                              column_num=0)
        # craftable results entry
        self.results_entry = FancyEntryBox(self.craftables_edit_frame,
                                           row_num=self.craftables_edit_frame.get_available_row(),
                                           column_num=0,
                                           string=self.lang['CRAFTABLE']['results'])
        # craftable category combobox
        self.category_combobox = FancyComboBox(self.craftables_edit_frame,
                                               row_num=self.craftables_edit_frame.get_available_row(),
                                               column_num=0,
                                               string=self.lang['CRAFTABLE']['category'])
        # crafting type combobox
        self.crafting_type_combobox = FancyComboBox(self.craftables_edit_frame,
                                                    row_num=self.craftables_edit_frame.get_available_row(),
                                                    column_num=0,
                                                    string=self.lang['CRAFTABLE']['crafting_type'])
        # craftable description box
        self.description_box = FancyDescriptionBox(self.craftables_edit_frame,
                                                   row_num=self.craftables_edit_frame.get_available_row(),
                                                   column_num=0,
                                                   string=self.lang['CRAFTABLE']['description'])
        # apply changes button
        self.apply_button = tk.Button(self.craftables_edit_frame,
                                      text=self.lang['WIDGET']['apply'],
                                      command=self.apply_changes)
        self.apply_button.grid(row=self.craftables_edit_frame.get_available_row(),
                               column=0,pady=20,sticky='e')
    # sets list frame needed when applying changes
    def set_list_frame(self,list_frame):
        self.craftables_list_frame = list_frame
    # sets the lists for the comboboxes
    def set_boxlists(self,crafting_reqs_list,categories_list,crafting_types_list):
        self.crafting_reqs_list = crafting_reqs_list
        self.categories_list = categories_list
        self.crafting_types_list = crafting_types_list
        self.crafting_reqs_tree.set_boxlist(self.crafting_reqs_list)
        self.category_combobox.set_boxlist(self.categories_list)
        self.crafting_type_combobox.set_boxlist(self.crafting_types_list)
    # apply changes to edited craftable
    def apply_changes(self):
        new_name = self.name_entry.get_entry()
        # if the craftable's new name isn't blank
        if new_name != "" and new_name.isspace() == False:
            # and if size scale is enabled
            if self.scale_entry.is_checkbox_enabled() == True:
                size_scale = self.scale_entry.get_entry()
            else:
                size_scale = -1 # otherwise, don't set it in the jmod dict
            crafting_reqs = self.crafting_reqs_tree.get_entry()
            results = self.results_entry.get_entry()
            category = self.category_combobox.get_entry()
            crafting_type = self.crafting_type_combobox.get_entry()
            description = self.description_box.get_entry()
            # set changed craftable data in the jmod dict
            dictfuncs.set_craftable_data(self.get_jmod_dict(),
                                         self.get_jmod_version(),
                                         oldName=self.craftable_name,
                                         newName=new_name,
                                         size_scale=size_scale,
                                         crafting_reqs=crafting_reqs,
                                         results=results,
                                         category=category,
                                         crafting_type=crafting_type,
                                         description=description)
            self.craftable_name = new_name      # rename craftable to be reflected
            try:
                self.craftables_list_frame.show_item(self.craftable_name) # in listbox
            except AttributeError:
                InternalErrorMessage("List frame not binded OR missing dictfunc")
        else: # if the craftable's name has been changed to blank
            # show an error message saying that it can't be blank
            messagebox.showerror(title=self.lang['MESSAGEBOX']['error'],message=self.lang['CRAFTABLE']['blank'])
    # clears all entries
    def clear_entries(self):
        self.name_entry.clear()
        self.scale_entry.disable_spinbox()
        self.crafting_reqs_tree.clear()
        self.results_entry.clear()
        self.category_combobox.clear()
        self.crafting_type_combobox.clear()
        self.description_box.clear()
    # loads craftable data
    def load_data(self,craftable_name):
        self.craftable_name = craftable_name
        # retrieve craftable data from jmod dict
        scale = []
        crafting_reqs = []
        results = []
        category = []
        crafting_type = []
        description = []
        dictfuncs.get_craftable_data(self.get_jmod_dict(),
                                     self.get_jmod_version(),
                                     craftable_name=self.craftable_name,
                                     size_scale=scale,
                                     crafting_reqs=crafting_reqs,
                                     results=results,
                                     category=category,
                                     crafting_type=crafting_type,
                                     description=description)
        # set data as pre-existing entries
        self.name_entry.set_entry(self.craftable_name)
        if len(scale) == 1:
            self.scale_entry.set_entry(scale[0])
            self.scale_entry.enable_spinbox() # enable spinbox if loaded craftable has scale 
        else:
            self.scale_entry.disable_spinbox() # disable spinbox otherwise
        self.crafting_reqs_tree.set_entry(crafting_reqs[0])
        self.results_entry.set_entry(results[0])
        self.category_combobox.set_entry(category[0])
        self.crafting_type_combobox.set_entry(crafting_type[0])
        self.description_box.set_entry(description[0])