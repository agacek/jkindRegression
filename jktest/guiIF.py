
try:
    from gui.events import Events
    from gui.events import EventTypes
except:
    pass



class GuiIF( object ):
    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _fileCount = 0
    _fileIdx = 0
    _fileUnderTest = None
    _argUnderTest = None



    def __init__( self ):
        '''
        Constructor
        '''
        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def setFileCount( self, count ):
        self._fileCount = count


    def getFileCount( self ):
        return self._fileCount


    def setFileUnderTest( self, f ):
        self._fileUnderTest = f
        self._fileIdx += 1
        try:
            Events().update( EventTypes.FILE_UPDATE )
        except:
            pass


    def getFileUnderTest( self ):
        return self._fileUnderTest


    def getFileIdx( self ):
        return self._fileIdx


    def setArgUnderTest( self, arg ):
        self._argUnderTest = arg
        try:
            Events().update( EventTypes.ARG_UPDATE )
        except:
            pass


    def getArgUnderTest( self ):
        return self._argUnderTest
