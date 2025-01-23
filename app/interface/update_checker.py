import tkinter as tk
from tkinter import messagebox
from .about_window import get_editor_version
from ..lib import dictfuncs
import webbrowser
from urllib import request
import json

_UPDATE_URL = "https://api.github.com/repos/muffindelegate39423/jmod-crafting-editor/releases/latest"
_UPDATE_PAGE = "https://github.com/muffindelegate39423/jmod-crafting-editor/releases/latest"

# popup message that checks for program updates on github
class UpdateChecker:
    def __init__(self,CommonWidget,notify_no_updates):
        self.common = CommonWidget(parent=None,row_num=None,column_num=None) # can't inherit due to limitations with python
        self.lang = self.common.lang
        try: # connect to update url
            response = request.urlopen(_UPDATE_URL)
            response = response.read()
            response = response.decode("utf-8")
            test = json.loads(response)
            latest_version = test['name'].lstrip('v')
            current_version = get_editor_version()
            if latest_version != current_version: # if the latest version doesn't match current version
                # ask the user if they want to download the latest update
                download_update = messagebox.askyesno(title=self.lang['UPDATE']['title'],
                                                        message=self.lang['UPDATE']['new'])
                if download_update == True: # opens update page if the user wants to update
                    webbrowser.open_new_tab(_UPDATE_PAGE)
            else: # if program is on latest version...
                if notify_no_updates == True: # notify user that it is
                    messagebox.showinfo(title=self.lang['MESSAGEBOX']['info'],
                                        message=self.lang['UPDATE']['none'])
        except URLError:
            if notify_no_updates == True: # if there's a connection error, notify user
                messagebox.showerror(title=self.lang['MESSAGEBOX']['error'],
                                    message=self.lang['UPDATE']['no_connection'])