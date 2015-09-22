import tkinter as tk
import threading
from jktest import testsuite
from jktest.guiIF import GuiIF
from gui.events import Events
from gui.events import EventTypes
from gui.menu import MyMenu


class MainFrameGUI( tk.Frame ):
    '''
    This is the Main Window Frame for the Coding Standards GUI
    '''

    def __init__( self, parentFrame, root ):
        '''
        Constructor
        
        Arguments:
        parentFrame - The parent Frame of this window. If this is stand - alone
                      application then this would be root. If this is part
                      of a larger application then would be another frame
        root - The Tkinter root.
        '''

        tk.Frame.__init__( self, master = parentFrame )
        parentFrame.title( 'JKind Regression Test' )
        self._root = root

        # Create the Menu
        parentFrame.config( menu = MyMenu( self, root ) )

        # Set the default padding values
        py = 5
        row = 0

        # Add our widgets...
        tk.Label( self, text = 'FileCounter' ).grid( column = 0, row = row, sticky = tk.W )
        self._fileCounterEdit = tk.Entry( self, width = 10 )
        self._fileCounterEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        tk.Label( self, text = 'Current File' ).grid( column = 0, row = row, sticky = tk.W )
        self._currFileEdit = tk.Entry( self, width = 80 )
        self._currFileEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        tk.Label( self, text = 'Arguments' ).grid( column = 0, row = row, sticky = tk.W )
        self._argsEdit = tk.Entry( self, width = 80 )
        self._argsEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        tk.Label( self, text = 'Pass Count' ).grid( column = 0, row = row, sticky = tk.W )
        self._passEdit = tk.Entry( self, width = 10 )
        self._passEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        tk.Label( self, text = 'Fail Count' ).grid( column = 0, row = row, sticky = tk.W )
        self._failEdit = tk.Entry( self, width = 10 )
        self._failEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        self._execButton = tk.Button( master = self,
                                      text = 'Execute',
                                      width = 15,
                                      bg = 'light green',
                                      command = self._onExecButton )
        self._execButton.grid( column = 0, row = row, pady = py, sticky = tk.S )


        # Register the update methods
        Events().registerUpdateMethod( EventTypes.FILE_UPDATE, self._updateFile )
        Events().registerUpdateMethod( EventTypes.ARG_UPDATE, self._updateArgs )
        Events().registerUpdateMethod( EventTypes.RESULT_UPDATE, self._updateResults )
        Events().registerUpdateMethod( EventTypes.TEST_DONE, self._enableExecButton )

        # Initial GUI update
        self.update()

        # Pack this frame to the parent root
        self.pack( side = tk.TOP )

        # Initialize the Pass/Fail counts
        self._updateResults()


    def _onExecButton( self ):
        self._execButton.configure( state = 'disabled', bg = 'light gray' )
        ExecThread().start()


    def _enableExecButton( self ):
        self._execButton.configure( state = 'normal', bg = 'light green' )


    def _updateFile( self ):
        s = str( GuiIF().getFileIdx() ) + ' / ' + str( GuiIF().getFileCount() )
        self._fileCounterEdit.delete( 0, tk.END )
        self._fileCounterEdit.insert( 0, s )

        self._currFileEdit.delete( 0, tk.END )
        self._currFileEdit.insert( 0, str( GuiIF().getFileUnderTest() ) )


    def _updateArgs( self ):
        self._argsEdit.delete( 0, tk.END )
        self._argsEdit.insert( 0, str( GuiIF().getArgUnderTest() ) )


    def _updateResults( self ):
        self._passEdit.delete( 0, tk.END )
        self._passEdit.insert( 0, str( GuiIF().getTestPass() ) )

        self._failEdit.delete( 0, tk.END )
        self._failEdit.insert( 0, str( GuiIF().getTestFail() ) )


class ExecThread( threading.Thread ):
    def run( self ):
        testsuite.runsuite()
