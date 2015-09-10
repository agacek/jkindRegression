import tkinter as tk
import threading
from test_runner import runner
from test_runner.logger import Logger
from test_runner.events import Events
from test_runner.events import EventTypes


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

        py = 5
        row = 0

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
        Events().registerUpdateMethod( EventTypes.GUI_UPDATE, self._updateGui )
        Events().registerUpdateMethod( EventTypes.TEST_DONE, self._enableExecButton )

        # Initial GUI update
        self.update()

        # Pack this frame to the parent root
        self.pack( side = tk.TOP )


    def _onExecButton( self ):
        # runner.runtest( 'c:/temp', False )
        self._execButton.configure( state = 'disabled', bg = 'light gray' )
        ExecThread().start()


    def _enableExecButton( self ):
        self._execButton.configure( state = 'normal', bg = 'light green' )


    def _updateGui( self ):
        s = str( Logger().fileIdx() ) + ' / ' + str( Logger().fileCount() )
        self._fileCounterEdit.delete( 0, tk.END )
        self._fileCounterEdit.insert( 0, s )

        self._argsEdit.delete( 0, tk.END )
        self._argsEdit.insert( 0, str( Logger().argumentUnderTest() ) )

        self._currFileEdit.delete( 0, tk.END )
        self._currFileEdit.insert( 0, str( Logger().fileUnderTest() ) )

        self._passEdit.delete( 0, tk.END )
        self._passEdit.insert( 0, str( Logger().passCount() ) )

        self._failEdit.delete( 0, tk.END )
        self._failEdit.insert( 0, str( Logger().failCount() ) )


class ExecThread( threading.Thread ):
    def run( self ):
        runner.runtest()
