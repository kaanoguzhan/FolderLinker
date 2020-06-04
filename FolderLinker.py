from enum import Enum
import os, ctypes

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, END
except:
    import Tkinter as tk
    import filedialog, messagebox, END

import pygubu


class FolderLinker:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        self.builder.add_from_file('uixml.ui')

        # Acquire UI objects
        self.mainwindow = builder.get_object('MainFrame')
        self.txtSourcePath = builder.get_object('Entry_1')
        self.txtDestinationPath = builder.get_object('Entry_2')
        self.txtFolderName = builder.get_object('Entry_3')
        self.chkButton1 = builder.get_object('Checkbutton_1')
        self.chkButton2 = builder.get_object('Checkbutton_2')
        self.chkButton3 = builder.get_object('Checkbutton_3')
        self.btnLinkFolders = builder.get_object('Button_1')
        self.lblSymblblolicBtn = builder.get_variable('lblsymbolic')

        callbacks = {
            'pickSource': self.pickSource,
            'pickDestination': self.pickDestination,
            'radioSelect1': self.radioSelect1,
            'radioSelect2': self.radioSelect2,
            'radioSelect3': self.radioSelect3,
            'linkFolders': self.linkFolders
        }
        self.builder.connect_callbacks(callbacks)

        self.mode = LinkMode.NONE

        import ctypes, os
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if is_admin:
            self.lblSymblblolicBtn.set("")
            self.chkButton2.config(state="normal")


    def pickSource(self, args):
        folder_selected = filedialog.askdirectory()
        if len(folder_selected) > 1:
            self.txtSourcePath.delete(0, END)
            self.txtSourcePath.insert(0, folder_selected)
            self.txtSourcePath.config(background="#FFFFFF")

    def pickDestination(self, args):
        folder_selected = filedialog.askdirectory()
        if len(folder_selected) > 1:
            self.txtDestinationPath.delete(0, END)
            self.txtDestinationPath.insert(0, folder_selected)
            self.txtDestinationPath.config(background="#FFFFFF")

    def radioSelect1(self):
        print("Selected mode: " + self.chkButton1.cget("text"))
        self.chkButton2.deselect()
        self.chkButton3.deselect()
        if self.mode != LinkMode.JUNCTION:
            self.mode = LinkMode.JUNCTION
            self.btnLinkFolders.config(state="normal")
            self.btnLinkFolders.config(background="#66bb6a")
            
        else:
            self.mode = LinkMode.NONE
            self.btnLinkFolders.config(state="disabled")
            self.btnLinkFolders.config(background="#BDBDBD")

    def radioSelect2(self):
        print("Selected mode: " + self.chkButton2.cget("text"))
        self.chkButton1.deselect()
        self.chkButton3.deselect()
        if self.mode != LinkMode.SYMBOLIC:
            self.mode = LinkMode.SYMBOLIC
            self.btnLinkFolders.config(state="normal")
            self.btnLinkFolders.config(background="#d4e157")
        else:
            self.mode = LinkMode.NONE
            self.btnLinkFolders.config(state="disabled")
            self.btnLinkFolders.config(background="#BDBDBD")

    def radioSelect3(self):
        print("Selected mode: " + self.chkButton3.cget("text"))
        self.chkButton1.deselect()
        self.chkButton2.deselect()
        if self.mode != LinkMode.HARD:
            self.mode = LinkMode.HARD
            self.btnLinkFolders.config(state="normal")
            self.btnLinkFolders.config(background="#ffa726")
        else:
            self.mode = LinkMode.NONE
            self.btnLinkFolders.config(state="disabled")
            self.btnLinkFolders.config(background="#BDBDBD")

    def linkFolders(self):
        print("Linking...\nSource:\"" + self.txtSourcePath.get()
              + "\"\nDestination:\"" + self.txtDestinationPath.get() + "\\" + self.txtFolderName.get() + "\"")

        link_mode = ""
        if self.mode == LinkMode.NONE:
            messagebox.showinfo("Error !", "You need to select a Link Type")
            self.chkButton1.flash()
            self.chkButton2.flash()
            self.chkButton3.flash()
        elif self.mode == LinkMode.JUNCTION:
            link_mode = "/J"
        elif self.mode == LinkMode.SYMBOLIC:
            link_mode = "/D"
        elif self.mode == LinkMode.HARD:
            link_mode = "/H"

        command = "mklink " + link_mode + " " + self.txtDestinationPath.get().replace("/","\\") + "\\" + self.txtFolderName.get()+ " "+  self.txtSourcePath.get().replace("/","\\")
        print(command)
        os.system(command)

        print("DONE!\n")

    def run(self):
        self.mainwindow.mainloop()


class LinkMode(Enum):
    NONE = 0
    JUNCTION = 1
    SYMBOLIC = 2
    HARD = 3


if __name__ == '__main__':
    app = FolderLinker()
    app.run()
