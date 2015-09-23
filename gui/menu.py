
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from jktest.config import SetupConfig


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

        # Test Menu
        testmenu = tk.Menu( self, tearoff = 0 )
        testmenu.add_command( label = 'Select File(s)', command = self._selectFiles )
        testmenu.add_command( label = 'Select Folder', command = self._selectFolder )
        testmenu.add_command( label = 'Select new XML Argument file', command = self._selectArgs )
        self.add_cascade( label = "Test Config", menu = testmenu )


    def _selectArgs( self ):
        opt = {}
        opt['filetypes'] = [( 'xml files', '.xml' ), ( 'all files', '.*' )]
        opt['parent'] = self
        opt['title'] = 'Select XML Argument file'
        opt['multiple'] = False

        f = askopenfilename( **opt )
        SetupConfig().setTestArguments( f )


    def _selectFolder( self ):
        folder = askdirectory()
        SetupConfig().setTestFiles( folder, recurse = False )


    def _selectFiles( self ):
        opt = {}
        opt['filetypes'] = [( 'lus files', '.lus' ), ( 'all files', '.*' )]
        opt['parent'] = self
        opt['title'] = 'Select lus file(s)'
        opt['multiple'] = True

        files = askopenfilename( **opt )
        SetupConfig().setTestFiles( list( files ), recurse = False )

