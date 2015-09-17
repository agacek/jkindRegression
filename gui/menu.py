
import tkinter as tk


class MyMenu( tk.Menu ):
    '''
    classdocs
    '''


    def __init__( self, masterFrame, root ):
        '''
        Constructor
        '''
        tk.Menu.__init__( self, masterFrame )

        # Save the root and Master Frame to create windows
        self._root = root
        self._masterFrame = masterFrame

        # File Menu
        filemenu = tk.Menu( self, tearoff = 0 )
        filemenu.add_command( label = "Quit!", command = root.destroy )
        self.add_cascade( label = "File", menu = filemenu )

