import tkinter as tk
from tkinter import messagebox
from ..lib import dictfuncs

# window shown for pending craftables to delete
class DeleteWindow:
    def __init__(self,CommonWidget,FrameWidget,listbox,selected_items,selected_label,clear_edit_frame):
        self.common = CommonWidget(parent=None,row_num=None,column_num=None) # can't inherit due to limitations with python
        self.lang = self.common.lang
        # listbox to manipulate
        self.listbox = listbox
        # selected items
        self.selected_items = selected_items
        # selected item count
        self.count = len(self.selected_items)
        # selected label
        self.selected_label = selected_label
        # clear edit frame function
        self.clear_edit_frame = clear_edit_frame
        # window info
        self.root = tk.Toplevel()
        self.root.title(self.lang['WINDOW']['pending'])
        self.root.resizable(0,0)
        self.root.wait_visibility()
        self.root.grab_set()
        # pending frame
        pending_frame = FrameWidget(self.root)
        pending_frame.pack(padx=3,pady=3)
        # pending label
        pending_label = tk.Label(pending_frame,
                                 text=self.lang['CRAFTABLE']['pending'].format(
                                 newline='\n', count=self.count),
                                 font=('TkDefaultFont',9,'bold'))
        pending_label.pack()
        # pending listbox
        pending_list_var = tk.Variable(value=self.selected_items)
        pending_listbox = tk.Listbox(pending_frame,listvariable=pending_list_var)
        pending_listbox.pack(ipadx=50,ipady=50)
        # buttons
        button_frame = FrameWidget(self.root)
        button_frame.pack()
        delete_button = tk.Button(button_frame,
                                  text=self.lang['DELETE']['delete'],
                                  command=lambda:self.delete_craftables()).grid(
                                  row=0,column=button_frame.get_available_column())
        cancel_button = tk.Button(button_frame,
                                  text=self.lang['DELETE']['cancel'],
                                  command=lambda:self.root.destroy()).grid(
                                  row=0,column=button_frame.get_available_column())
        # window binds
        self.root.bind("<Return>",lambda event:self.delete_craftables())
        self.root.bind("<Escape>",lambda event:self.root.destroy())
    # asks if user wants to remove the items and, if so, remove them from listbox
    def delete_craftables(self):
        try:
            dictfuncs.remove_craftables(self.common.get_jmod_dict(),
                                        self.common.get_jmod_version(),
                                        self.selected_items)
            self.listbox.remove_item_names(self.selected_items)
        except (KeyError, ValueError):
            pass
        self.selected_label.clear()
        self.clear_edit_frame()
        self.root.destroy()