from tkinter import messagebox, filedialog
from .widgets import *
from ..lib import dictfuncs
import configparser, json, pathlib, os
from shutil import copyfile

# class with operations that are used to open the config file
class ConfigOpener(CommonWidget):
    def __init__(self):
        super().__init__(parent=None,row_num=None,column_num=None)
    # does the user want to continue opening
    # the unsupported config?
    def _continue_unsupported(self,config):
        # show warning that the config is unsupported
        messagebox.showwarning(title=self.lang['MESSAGEBOX']['warning'],
                               message=self.lang['CONFIGFILE']['unsupported'].format(
                               version=dictfuncs.get_jmod_version(config)))
        # ask if the user wants to continue opening it
        proceed = messagebox.askyesno(title=self.lang['MESSAGEBOX']['question'],
                                      message=self.lang['CONFIGFILE']['confirm_open'])
        return proceed
    # loads and process config (for self.launch_config, self.open_config, and self.quick_open_config)
    def _load_config(self,config_path):
        config = json.loads(open(config_path,'r',encoding='utf-8').read())
        # if config is version 49.6 or later
        if dictfuncs.supports_dynamic_crafting_types(dictfuncs.get_jmod_version(config)):
            # format dynamic crafting types for interface
            config = dictfuncs.format_crafting_types(config)
        return config
    # returns config when launching the program
    def launch_config(self,config_path):
        if config_path != "": # if this program has been used previously...
            try: # attempt to open the last config
                config = self._load_config(config_path)
                # check config if it's valid/supported
                if dictfuncs.is_valid_config(config) == False:
                    raise Exception # raise an exception if it's invalid
                # if it's valid but it has an unsupported jmod version,
                # show unsupported config prompt
                elif dictfuncs.is_supported_version(dictfuncs.get_jmod_version(config)) == False:
                    # if the user doesn't want to 
                    # open the unsupported config
                    if self._continue_unsupported(config) == False:
                        config = -1 # program will close by setting -1
            except: # if the file cannot be loaded...
                # show an error message
                messagebox.showerror(title=self.lang['MESSAGEBOX']['error'],
                                     message=self.lang['CONFIGFILE']['cannot_read'])
                config = self.open_config() # and let the user open
                                            # another config file
        else: # otherwise, greet upon first launch
            messagebox.showinfo(title=self.lang['MESSAGEBOX']['info'], 
                                message=self.lang['CONFIGFILE']['select'])
            config = self.open_config() # and let the user open
                                        # a config from file
        return config
    # returns config when opening from file
    def open_config(self):
        valid = False
        while valid == False: # while config file is invalid/not opened
            open_from = filedialog.askopenfilename( # let the user open a config file
                defaultextension=".txt",
                filetypes=[(self.lang['FILETYPE']['jmod'],"*.txt"),
                (self.lang['FILETYPE']['all'],"*.*")])
            if open_from:
                config = self._load_config(open_from)
                # if it's a valid config
                if dictfuncs.is_valid_config(config) == True:
                    valid = True # set valid boolean as true
                    # if the config version is unsupported
                    if dictfuncs.is_supported_version(dictfuncs.get_jmod_version(config)) == False:
                        # let the user decide to still open it
                        proceed = self._continue_unsupported(config)
                        # if the user doesn't wants to continue
                        if proceed == False:
                            return -1 # close program
                    self.setup['DEFAULT']['path'] = open_from # set path to new one
                    return config
                else: # otherwise, show an error message saying it's invalid
                    messagebox.showerror(title=self.lang['MESSAGEBOX']['error'],
                                         message=self.lang['CONFIGFILE']['invalid'])
                    # and loop
            else:
                return -1 # close program
    # quick open config without doing any additional checks
    def quick_open_config(self,config_path):
        config = self._load_config(config_path)
        return config
    # saves config to specified path
    def save_config(self,config,path):
        config_path = pathlib.Path(path)
        config_dir = os.path.dirname(path)
        # if config already exists, back it up
        if config_path.is_file() == True:
            temp = config_path.parts[-1]
            temp = os.path.splitext(temp)
            temp = os.path.join(config_dir,temp[0]+"_BAK"+temp[1])
            copyfile(config_path,temp)
        # if jmod version >= 49.6, then fix crafting types before saving
        if dictfuncs.supports_dynamic_crafting_types(dictfuncs.get_jmod_version(config)):
            config = dictfuncs.fix_crafting_types(config)
        # saves config
        with open(config_path,'w',encoding='utf8') as f:
            json.dump(config,f,indent=4,ensure_ascii=False)
    # lets user specify path to save config to
    def save_config_as(self,config,curPath):
        temp = pathlib.Path(curPath)
        file_name = temp.parts[-1]
        save_to = filedialog.asksaveasfilename(
            initialfile=file_name,
            defaultextension=".txt",
            filetypes=[(self.lang['FILETYPE']['jmod'],"*.txt"),(self.lang['FILETYPE']['all'],"*.*")])
        # if path has been specified by user
        if save_to: # save config to that path
            self.save_config(config,save_to)
            self.setup['DEFAULT']['path'] = save_to # set path to new one
            return True # let caller know that user has saved
        else:
            return False