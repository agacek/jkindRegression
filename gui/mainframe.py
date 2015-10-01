import tkinter as tk
import threading
from tkinter import messagebox
from jktest import testsuite
from jktest.guiIF import GuiIF
from jktest.config import SetupConfig
from gui.events import Events
from gui.events import EventTypes
from gui.menu import MyMenu


class MainFrameGUI( tk.Frame ):
    '''
    **Public Class**
    
    This is the Main Window Frame for the Tkinter GUI
    
    '''

    def __init__( self, parentFrame, root ):
        '''
        **Constructor**
        
        Builds the GUI window and registers update methods with
        the Events class.
        
        :param parentFrame: The parent Frame of this window. If this is
                            a standalone application then this would be root.
                            If this is part of a larger application then would
                            be another frame
        :type parentFrame: tkinter.Toplevel
        :param root: The Tkinter root.
        :type root: tkinter.Tk
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

        tk.Label( self, text = 'SubTest Pass Count' ).grid( column = 0, row = row, sticky = tk.W )
        self._passEdit = tk.Entry( self, width = 10 )
        self._passEdit.grid( column = 1, row = row, sticky = tk.W, pady = py )
        row += 1

        tk.Label( self, text = 'SubTest Fail Count' ).grid( column = 0, row = row, sticky = tk.W )
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
        '''
        **Private Method**
        
        Handler for Execute Button pressed.
        Checks that test file(s) have been selected.
        Resets the data in the GUI Interface class and the GUI fields.
        Disables the Execute Button widget.
        Initiates a new thread to run the Regression Test Suite.
        
        :return: n/a:
        
        '''

        # Test that we have files to test
        f = SetupConfig().getTestFiles()
        if( 
           isinstance( f, list ) == False or
           len( f ) < 1
           ):
            messagebox.showerror( 'Uh-oh', 'No File(s) to test specified' )
            return

        self._execButton.configure( state = 'disabled', bg = 'light gray' )
        GuiIF().reset()
        self._updateResults()
        ExecThread().start()


    def _enableExecButton( self ):
        '''
        **Private Method**
        
        Enables the Execute Button widget.
        Registered with the Events class and called when the test completes.
        
        :return: n/a:
        
        '''
        self._execButton.configure( state = 'normal', bg = 'light green' )


    def _updateFile( self ):
        '''
        **Private Method**
        
        Updates the File Count and File Under Test widgets.
        Registered with the Events class and called by the test execution.
        
        :return: n/a:
        
        '''
        s = str( GuiIF().getFileIdx() ) + ' / ' + str( GuiIF().getFileCount() )
        self._fileCounterEdit.delete( 0, tk.END )
        self._fileCounterEdit.insert( 0, s )

        self._currFileEdit.delete( 0, tk.END )
        self._currFileEdit.insert( 0, str( GuiIF().getFileUnderTest() ) )


    def _updateArgs( self ):
        '''
        **Private Method**
        
        Updates the Argument Under Test widget.
        Registered with the Events class and called by the test execution.
        
        :return: n/a:
        
        '''
        self._argsEdit.delete( 0, tk.END )
        self._argsEdit.insert( 0, str( GuiIF().getArgUnderTest() ) )


    def _updateResults( self ):
        '''
        **Private Method**
        
        Updates the Pass and Fail Count widgets.
        Registered with the Events class and called by the test execution.
        
        :return: n/a:
        
        '''
        self._passEdit.delete( 0, tk.END )
        self._passEdit.insert( 0, str( GuiIF().getPassCount() ) )

        self._failEdit.delete( 0, tk.END )
        self._failEdit.insert( 0, str( GuiIF().getFailCount() ) )


class ExecThread( threading.Thread ):
    '''
    **Public Class**
    
    Container to launch a new thread and run the Regression Test Suite.
    
    '''
    def run( self ):
        '''
        **Public Method**
        
        Do not call directly. Started by threading.Thread.start()
        
        '''
        testsuite.runsuite()
