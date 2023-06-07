from . import widgets
import tkinter, configparser

class PendingWindow:
    def __init__(self,parent,l,selectedCraftables):
        # parent
        self.Parent = parent
        # lang
        self.lang = l
        # selected craftables
        self.selected_craftables = selectedCraftables
        # display
        self.display()

    def display(self):
        # window
        self.root = tkinter.Toplevel()
        self.root.title(self.lang["WINDOW"]["pending"])
        self.root.geometry("350x475")
        self.root.resizable(0,0)
        self.root.wait_visibility()
        self.root.grab_set()
        # pending label
        pending_label = tkinter.Label(self.root,text=self.lang["CRAFTABLE"]["pending"].format(newline = "\n"),font=("TkDefaultFont",9,"bold"))
        pending_label.pack()
        # pending listbox
        pending_listbox = widgets.PendingListbox(self.root,2,0,self.selected_craftables)
        # buttons
        buttonFrame = tkinter.Frame(self.root)
        buttonFrame.pack(side="bottom")
        deleteButton = tkinter.Button(buttonFrame,text="Delete",command=lambda:self.delete_craftable()).grid(row=0,column=0)
        cancelButton = tkinter.Button(buttonFrame,text="Cancel",command=lambda:self.root.destroy()).grid(row=0,column=1)

    def delete_craftable(self):
        count = len(self.selected_craftables)
        proceed = tkinter.messagebox.askyesno(title=self.lang["MESSAGEBOX"]["question"],message=self.lang["CRAFTABLE"]["delete"].format(count = str(count)))
        if proceed == True:
            print("ping")
        self.root.destroy()