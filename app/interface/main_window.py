import tkinter as tk
from tkinter import messagebox
from .widgets import *
from .config_opener import *
from .about_window import *
from .update_checker import *
from ..lib import dictfuncs
import configparser

# main window of the editor
class MainWindow(CommonWidget):
    def __init__(self):
        super().__init__(parent=None,row_num=None,column_num=None)
        # check for program updates if enabled
        if self.setup['DEFAULT']['updates'] == "True":
            UpdateChecker(CommonWidget,notify_no_updates=False)
        # window info
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title(self.lang['WINDOW']['main'])
        # path label
        self.path_label = PathDisplay(self.root,row_num=0,column_num=0)
        # config version label
        self.version_label_var = tk.StringVar()
        self.version_label = tk.Label(self.root,
                                      textvariable=self.version_label_var,
                                      font=('TkDefaultFont',8,'bold'))
        self.version_label.grid(row=1,column=0,sticky='w')
        # main frame
        self.main_frame = FrameWidget(self.root)
        self.main_frame.grid(row=2,column=0)
        # craftables list frame
        self.craftables_list_frame = CraftablesListFrame(self.main_frame,row_num=0,column_num=0)
        # craftables edit frame
        self.craftables_edit_frame = CraftablesEditFrame(self.main_frame,row_num=0,column_num=1)
        # bind craftable frames
        self.craftables_list_frame.set_edit_frame(self.craftables_edit_frame)
        self.craftables_edit_frame.set_list_frame(self.craftables_list_frame)
        # command menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # command button frame
        self.button_frame = FrameWidget(self.root)
        self.button_frame.grid(row=3,column=0,padx=5,ipady=5)
        # constant command button dimensions
        COMMAND_WIDTH = 20
        COMMAND_HEIGHT = 2
        # == COMMAND BUTTONS ==
        # command: open config
        self.open_button = tk.Button(self.button_frame,
                                     width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                     text=self.lang["COMMAND"]["open"],
                                     command=self.open_config)
        self.open_button.grid(row=0,column=0)
        # command: save config
        self.save_button = tk.Button(self.button_frame,
                                     width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                     text=self.lang["COMMAND"]["save"],
                                     command=self.save_config)
        self.save_button.grid(row=0,column=1)
        # command: save config as
        self.save_as_button = tk.Button(self.button_frame,
                                       width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                       text=self.lang["COMMAND"]["save_as"],
                                       command=self.save_config_as)
        self.save_as_button.grid(row=0,column=2)
        # command: new craftable
        self.new_button = tk.Button(self.button_frame,
                                    width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                    text=self.lang["COMMAND"]["new"],
                                    command=self.create_new_craftable)
        self.new_button.grid(row=1,column=0)
        # command: delete craftables
        self.delete_button = tk.Button(self.button_frame,
                                       width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                       text=self.lang["COMMAND"]["delete"],
                                       command=self.delete_craftables)
        self.delete_button.grid(row=1,column=1)
        # command: sort craftables
        self.sort_button = tk.Button(self.button_frame,
                                       width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                       text=self.lang["COMMAND"]["sort"],
                                       command=self.sort_craftables)
        self.sort_button.grid(row=1,column=2)
        # command: exit program
        self.exit_button = tk.Button(self.button_frame,
                                     width=COMMAND_WIDTH,height=COMMAND_HEIGHT,
                                     text=self.lang["COMMAND"]["exit"],
                                     command=self.exit)
        self.exit_button.grid(row=2,column=1)
        # ======= MENUS =======
        # file menu
        self.file_menu = tk.Menu(self.menu_bar,tearoff=False)
        self.menu_bar.add_cascade(
            label=self.lang['MENU']['file'],
            menu=self.file_menu)
        self.file_menu.add_command(label=self.lang['COMMAND']['open'],command=self.open_config)
        self.file_menu.add_command(label=self.lang['COMMAND']['save'],command=self.save_config)
        self.file_menu.add_command(label=self.lang['COMMAND']['save_as'],command=self.save_config_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.lang['COMMAND']['exit'],command=self.exit)
        # edit menu
        self.edit_menu = tk.Menu(self.menu_bar,tearoff=False)
        self.menu_bar.add_cascade(
            label=self.lang['MENU']['edit'],
            menu=self.edit_menu)
        self.edit_menu.add_command(label=self.lang['COMMAND']['new'],command=self.create_new_craftable)
        self.edit_menu.add_command(label=self.lang['COMMAND']['delete'],command=self.delete_craftables)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self.lang['COMMAND']['sort'],command=self.sort_craftables)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self.lang['WIDGET']['apply'],command=self.craftables_edit_frame.apply_changes)
        # help menu
        self.help_menu = tk.Menu(self.menu_bar,tearoff=False)
        self.menu_bar.add_cascade(
            label=self.lang['MENU']['help'],
            menu=self.help_menu)
        self.help_menu.add_command(label=self.lang['MENU']['updates'],command=self.check_for_updates)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=self.lang['MENU']['about'],command=self.open_about_window)
        # =====================
        # set data
        self.set_data()
        # display window
        self.root.mainloop()
    # sets data for widgets
    def set_data(self):
        # clear old data
        self.craftables_list_frame.clear_selection()
        self.craftables_edit_frame.clear_entries()
        # saves new config path to setup.ini
        save_setup()
        self.path_label.set_path(self.setup['DEFAULT']['path'])
        # display config version
        self.version_label_var.set(self.lang["WIDGET"]['jmod_version'].format(version=self.get_jmod_version()))
        # set craftables for display in listbox
        self.craftables_list_frame.set_craftables(dictfuncs.get_craftable_names(self.get_jmod_dict(),
                                                                                self.get_jmod_version()))
        # set boxlists in the craftables edit frame
        self.craftables_edit_frame.set_boxlists(crafting_reqs_list=dictfuncs.get_crafting_reqs(self.get_jmod_dict(),self.get_jmod_version()),
                                                categories_list=dictfuncs.get_categories(self.get_jmod_dict(),self.get_jmod_version()),
                                                crafting_types_list=dictfuncs.get_crafting_types(self.get_jmod_dict(),self.get_jmod_version()))
    # lets the user open a config from file
    def open_config(self):
        config_opener = ConfigOpener()
        config = config_opener.open_config()
        if config != -1:
            set_jmod_dict(config)
            self.set_data() # reload data
    # saves current config
    def save_config(self):
        config_saver = ConfigOpener()
        config_saver.save_config(self.get_jmod_dict(),self.setup['DEFAULT']['path'])
    # saves current config to a specified path
    def save_config_as(self):
        config_saver = ConfigOpener()
        is_saved = config_saver.save_config_as(self.get_jmod_dict(),self.setup['DEFAULT']['path'])
        if is_saved == True: # if the user did save
            set_jmod_dict(config_saver.quick_open_config(self.setup['DEFAULT']['path'])) # reload config in new path
            self.set_data()
    # creates new craftable
    def create_new_craftable(self):
        dictfuncs.create_new_craftable(self.get_jmod_dict(),
                                       self.get_jmod_version(),
                                       self.lang['CRAFTABLE']['new'])
        self.craftables_list_frame.reload_craftables()
        self.craftables_list_frame.show_item(self.lang['CRAFTABLE']['new'])
    # deletes selected craftables
    def delete_craftables(self):
        self.craftables_list_frame.open_delete_window()
    # opens "about program" window
    def open_about_window(self):
        AboutWindow()
    # checks for editor updates on github
    def check_for_updates(self):
        UpdateChecker(CommonWidget,notify_no_updates=True)
    # sorts craftables by name
    def sort_craftables(self):
        # ask the user if they really want to sort
        confirm_sort = messagebox.askyesno(title=self.lang['MESSAGEBOX']['question'],
                                           message=self.lang['CRAFTABLE']['sort'])
        if confirm_sort == True: # if the user wants to sort, let it sort
            temp = self.get_jmod_dict()
            dictfuncs.sort_craftables(temp,self.get_jmod_version())
            set_jmod_dict(temp)
            self.craftables_list_frame.reload_craftables()
    # terminates program
    def exit(self):
        exit()