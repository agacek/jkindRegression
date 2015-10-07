'''
This module provides the entry point to launch the GUI.

'''
from tkinter import Tk
from .mainframe import MainFrameGUI
from .mainframe import GuiReturnVal


def launchGUI():
    '''
    **Public Function**
    
    Instantiates Tkinter and creats the GUI.
    
    .. warning::
        This function directly calls the Tkinter mainloop() method, which does
        not exit. You must create your own thread and then call this function
        if desired.
        
    :return: Returns flag indicating whether the LAST execution of JKind was
             successful or not.
    :rtype: bool
    
    '''
    root = Tk()
    MainFrameGUI( parentFrame = root, root = root )
    root.mainloop()
    return GuiReturnVal.rv
