
from tkinter import Tk
from .mainframe import MainFrameGUI


def launchGUI( path, recurse ):
    root = Tk()
    MainFrameGUI( parentFrame = root, root = root )
    root.mainloop()
