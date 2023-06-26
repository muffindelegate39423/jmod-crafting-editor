import tkinter as tk
from .widgets import *

_EDITOR_VERSION = "0.2.0-prerelease"
_COPYRIGHT_YEARS = "2023"
_AUTHOR = "muffindelegate39423"
_GITHUB_LINK = "https://github.com/muffindelegate39423/jmod-crafting-editor"

# about program window
class AboutWindow(CommonWidget):
    def __init__(self):
        super().__init__(parent=None,row_num=None,column_num=None)
        # window info
        self.root = tk.Toplevel()
        self.root.resizable(0,0)
        self.root.title(self.lang['WINDOW']['about'])
        self.root.wait_visibility()
        self.root.grab_set()
        # about frame
        self.about_frame = FrameWidget(self.root)
        self.about_frame.pack(padx=5,pady=5)
        # program name label
        self.program_label = tk.Label(self.about_frame,
                                      text=self.lang['ABOUT']['program'],
                                      font=('TkDefaultFont',15,'bold'))
        self.program_label.pack()
        # version label
        self.version_label = tk.Label(self.about_frame,
                                      text=self.lang['ABOUT']['version'].format(
                                      version=_EDITOR_VERSION),
                                      font=('TkDefaultFont',10,'bold'))
        self.version_label.pack()
        # github label
        self.github_label = HyperlinkLabel(self.about_frame,
                                           text=self.lang['ABOUT']['github'],
                                           link=_GITHUB_LINK)
        self.github_label.pack()
        # copyright label
        self.copyright_label = tk.Label(self.about_frame,
                                        text=self.lang['ABOUT']['copyright'].format(
                                        years=_COPYRIGHT_YEARS,author=_AUTHOR),
                                        font=('TkDefaultFont',10))
        self.copyright_label.pack()
        # disclaimer label
        self.disclaimer_label = tk.Label(self.about_frame,
                                         text=self.lang['ABOUT']['disclaimer'],
                                         font=('TkDefaultFont',8))
        self.disclaimer_label.pack()
        # additional credits label
        self.credits_label = tk.Label(self.about_frame,
                                      text=self.lang['ABOUT']['credits'],
                                      font=('TkDefaultFont',8))
        self.credits_label.pack()
        # window binds
        self.root.bind("<Escape>",lambda event:self.root.destroy())