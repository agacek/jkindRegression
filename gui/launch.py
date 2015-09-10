
from tkinter import Tk
from .mainframe import MainFrameGUI


def launchGUI():
    root = Tk()
    MainFrameGUI( parentFrame = root, root = root )
    root.mainloop()
