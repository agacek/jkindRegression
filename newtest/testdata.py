

class TestData( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _fileList = None
    _argsList = None


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def setFiles( self, fileList ):
        self._fileList = fileList


    def popFile( self ):
        return self._fileList.pop()


    def fileCount( self ):
        return len( self._fileList )


    def setArguments( self, argumentsList ):
        self._argsList = argumentsList


    def popArgument( self ):
        self._argsList.pop()


