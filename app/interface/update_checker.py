import tkinter as tk
from tkinter import messagebox
from .about_window import get_editor_version
from ..lib import dictfuncs
import webbrowser
# attempt to import the non-builtin requests module
try:
    import requests
    not_installed = False
except ImportError:
    not_installed = True

_UPDATE_URL = "https://api.github.com/repos/muffindelegate39423/jmod-crafting-editor/releases/latest"
_UPDATE_PAGE = "https://github.com/muffindelegate39423/jmod-crafting-editor/releases/latest"

# popup message that checks for program updates on github
class UpdateChecker:
    def __init__(self,CommonWidget):
        self.common = CommonWidget(parent=None,row_num=None,column_num=None) # can't inherit due to limitations with python
        self.lang = self.common.lang
        if not_installed == False: # if the requests module is installed
            try: # connect to update url
                test = requests.get(_UPDATE_URL)
                latest_version = test.json()['name'].lstrip('v')
                current_version = get_editor_version()
                if latest_version != current_version: # if the latest version doesn't match current version
                    # ask the user if they want to download the latest update
                    download_update = messagebox.askyesno(title=self.lang['UPDATE']['title'],
                                                          message=self.lang['UPDATE']['new'])
                    if download_update == True: # opens update page if the user wants to update
                        webbrowser.open_new_tab(_UPDATE_PAGE)
            except requests.exceptions.ConnectionError:
                pass # skip update check if there's connection error
        else: # show a warning if the module isn't installed
            messagebox.showwarning(title=self.lang['MESSAGEBOX']['warning'],
                                   message=self.lang['UPDATE']['missing'])