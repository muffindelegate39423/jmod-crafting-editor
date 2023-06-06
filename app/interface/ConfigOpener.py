from ..lib import dictfuncs
import tkinter.messagebox, tkinter.filedialog

class ConfigOpener:
    def __init__(self,ini,s,l):
        self.setup_ini = ini
        self.setup = s
        self.lang = l
        self.jmod_config_txt = self.setup["DEFAULT"]["path"]

    def launch_reading_config(self):
        try:
            if self.jmod_config_txt == "":
                tkinter.messagebox.showinfo(title=self.lang["MESSAGEBOX"]["info"],message=self.lang["CONFIGFILE"]["select"])
                self.open_config()
            elif dictfuncs.is_valid_config(self.jmod_config_txt) == False:
                raise FileNotFoundError
        except FileNotFoundError:
            tkinter.messagebox.showerror(title=self.lang["MESSAGEBOX"]["error"],message=self.lang["CONFIGFILE"]["cannot_read"])
            self.open_config()

    def open_config(self):
        valid = False
        while valid == False:
            self.jmod_config_txt = tkinter.filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[(self.lang["FILETYPE"]["jmod"],"*.txt"),(self.lang["FILETYPE"]["all"],"*.*")]
            )
            if not self.jmod_config_txt:
                exit()
            else:
                if dictfuncs.is_valid_config(self.jmod_config_txt) == True:
                    self.setup["DEFAULT"]["path"] = self.jmod_config_txt
                    self.setup.write(open(self.setup_ini,'w'))
                    valid = True
                else:
                    tkinter.messagebox.showerror(title=self.lang["MESSAGEBOX"]["error"],message=self.lang["CONFIGFILE"]["invalid"])