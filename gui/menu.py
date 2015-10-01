
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from jktest.config import SetupConfig
import os


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
        filemenu.add_command( label = 'Quit!', command = root.destroy )
        self.add_cascade( label = 'File', menu = filemenu )

        # Test Menu
        testmenu = tk.Menu( self, tearoff = 0 )
        testmenu.add_command( label = 'Select File(s)', command = self._selectFiles )
        testmenu.add_command( label = 'Select Folder', command = self._selectFolder )
        testmenu.add_command( label = 'Select new XML Argument file', command = self._selectArgs )
        self.add_cascade( label = 'Test Config', menu = testmenu )

        # Log Menu
        logmenu = tk.Menu( self, tearoff = 0 )
        logmenu.add_command( label = 'Choose Log File', command = self._setLogFile )
        logmenu.add_command( label = 'Log to stdout', command = self._logStdOut )
        self.add_cascade( label = 'Log Options', menu = logmenu )

        # View Menu
        viewmenu = tk.Menu( self, tearoff = 0 )
        viewmenu.add_command( label = 'Show Test Options', command = self._showOptions )
        self.add_cascade( label = 'View', menu = viewmenu )


    def _logStdOut( self ):
        SetupConfig().setLogFile( None )

    def _setLogFile( self ):
        opt = {}
        opt['filetypes'] = [( 'text files', '.txt' ), ( 'all files', '*.*' )]
        opt['parent'] = self
        opt['title'] = 'Save Log file'

        f = asksaveasfilename( **opt )
        if( os.path.exists( os.path.dirname( f ) ) == False ):
            messagebox.showerror( 'Uh-oh', 'No Log File Selected' )
        else:
            SetupConfig().setLogFile( f )


    def _selectArgs( self ):
        opt = {}
        opt['filetypes'] = [( 'xml files', '.xml' ), ( 'all files', '.*' )]
        opt['parent'] = self
        opt['title'] = 'Select XML Argument file'
        opt['multiple'] = False

        f = askopenfilename( **opt )
        if( os.path.exists( f ) == False ):
            messagebox.showerror( 'Uh-oh', 'No Argument XML File Selected' )
        else:
            SetupConfig().setTestArguments( f )


    def _selectFolder( self ):
        folder = askdirectory()
        if( os.path.exists( folder ) == False ):
            messagebox.showerror( 'Uh-oh', 'No Folder Selected' )
        else:
            SetupConfig().setTestFiles( folder, recurse = False )


    def _selectFiles( self ):
        opt = {}
        opt['filetypes'] = [( 'lus files', '.lus' ), ( 'all files', '.*' )]
        opt['parent'] = self
        opt['title'] = 'Select lus file(s)'
        opt['multiple'] = True

        files = askopenfilename( **opt )
        if( isinstance( files, tuple ) ):
            SetupConfig().setTestFiles( list( files ), recurse = False )
        else:
            messagebox.showerror( 'Uh-oh', 'No lus File(s) Selected' )


    def _showOptions( self ):
        s = 'TEST OPTIONS:\n\n'

        # File(s)
        s += 'File(s): \n'
        lst = SetupConfig().getTestFiles()
        if( isinstance( lst, list ) == True ):
            for each in lst:
                if( isinstance( each, str ) == True ):
                    s += each + '\n'
        else:
            s += 'None\n'
        s += '\n'

        # Arguments
        s += 'Arguments: \n'
        lst = SetupConfig().getTestArguments()
        if( isinstance( lst, list ) == True ):
            for each in lst:
                if( isinstance( each, str ) == True ):
                    s += each + '\n'
        else:
            s += 'Default\n'
        s += '\n'

        # Log File
        s += 'Log File: \n'
        logF = SetupConfig().getLogFile()
        if( isinstance( logF, str ) == True ):
            s += logF
        else:
            s += 'None <console>'

        messagebox.showinfo( 'Config', s )

