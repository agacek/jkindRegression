'''
This module contains the GUI Interface class definition.
The GUI Interface class is responsible for transferring data between the
tests running here in the jktest package and the GUI in the gui package.

'''

try:
    from gui.events import Events
    from gui.events import EventTypes
except:
    pass



class GuiIF( object ):
    '''
    **Public Class**
    
    This class serves as the interface between the tests and the GUI.
    Data pertaining to the test runs are sent to the GUI using the Events
    class. Sending data to the GUI via an Event is somewhat recursive as
    the Events register update methods in the GUI, which in turn call back
    to retrieve data from this class. The GUI and the tests should be 
    running in different threads so that the GUI updates are seen as 
    they occur.
        
    This class implements the **Borg** Design Pattern. This DP is similar to a 
    Singleton, except that it is explicitly instantiated and contains shared
    data. Each instantiation is a unique object but all objects share the internal
    __dict__ and thus all share the data.
    
    '''

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _fileCount = 0
    _fileIdx = 0
    _fileUnderTest = None
    _argUnderTest = None
    _passCount = 0
    _failCount = 0


    def __init__( self ):
        '''
        **Constructor**
        
        Sets the shared state per the Borg Design Pattern.
        
        '''
        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def reset( self ):
        '''
        **Public Method**
        
        Resets the internal shared data to the default state.
        Typically called before starting test execution from the GUI.
        
        :return: n/a:
        
        '''
        self._fileCount = 0
        self._fileIdx = 0
        self._passCount = 0
        self._failCount = 0


    def setFileCount( self, count ):
        '''
        **Public Method**
        
        Sets the file count. Should be the number of files specified
        or discovered.
        
        Typically set before the TestSuite is run.
        
        :param count: Number of files specified or discovered
        :type count: int
        
        :return: n/a:
        
        '''
        self._fileCount = count


    def getFileCount( self ):
        '''
        **Public Method**
        
        Returns the value of the file count previously set in the 
        complementary setter method.
        
        :return: Value of the file count
        :rtype: int
        
        '''
        return self._fileCount


    def setFileUnderTest( self, fname ):
        '''
        **Public Method**
        
        Set the name of the file under test.
        Typically set in the individual Test Cases.
        
        Increments the File Index data member that serves as an internal
        counter of files run.
        
        Triggers the GUI update method if registered.
        
        :param fname: name of the file under test
        :type fname: str
        
        :return: n/a:
        
        '''
        self._fileUnderTest = fname
        self._fileIdx += 1
        try:
            Events().update( EventTypes.FILE_UPDATE )
        except:
            pass


    def getFileUnderTest( self ):
        '''
        **Public Method**
        
        Returns the name of the file under test previously set in the 
        complementary setter method.
                
        :rtype: str
        
        '''

        return self._fileUnderTest


    def getFileIdx( self ):
        '''
        **Public Method**
        
        Returns the File Index. This is a running count of the number of files
        tested to this point.
        
        :rtype: int
        
        '''
        return self._fileIdx


    def setArgUnderTest( self, arg ):
        '''
        **Public Method**
        
        Sets the string of the argument set under test.
        Typically set in the Test Cases as each argument set is run.
        
        Triggers the GUI update method if registered.
        
        :param arg: argument string under test
        :type arg: str
        
        :return: n/a:
        
        '''
        self._argUnderTest = arg
        try:
            Events().update( EventTypes.ARG_UPDATE )
        except:
            pass


    def getArgUnderTest( self ):
        '''
        **Public Method**
        
        Returns the string of the argument under test.
        
        :rtype: string
        
        '''
        return self._argUnderTest


    def logSubTestResult( self, PassOrFail ):
        if( PassOrFail == True ):
            self._passCount += 1
        else:
            self._failCount += 1
        Events().update( EventTypes.RESULT_UPDATE )


    def getTestPass( self ):
        return self._passCount


    def getTestFail( self ):
        return self._failCount


    def signalSuiteComplete( self ):
        try:
            Events().update( EventTypes.TEST_DONE )
        except:
            pass
