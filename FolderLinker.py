import pygubu

try:
    import tkinter as tk
    from tkinter import filedialog,END
except:
    import Tkinter as tk
    import tkMessageBox as filedialog,END


class FolderLinker:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        self.builder.add_from_file('uixml.ui')

        # Acquire UI objects
        self.mainwindow = builder.get_object('MainFrame')
        self.txtSourcePath = builder.get_object('Entry_1')

        callbacks = {
            'comm': self.clicked,
            'comm1': self.clicked
        }
        self.builder.connect_callbacks(callbacks)



    def clicked(self):
        folder_selected = filedialog.askdirectory()
        self.txtSourcePath.delete(0, END)
        self.txtSourcePath.insert(0, folder_selected)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = FolderLinker()
    app.run()