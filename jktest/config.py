import os
import fnmatch
import xml.dom.minidom
from itertools import product
from jktest.guiIF import GuiIF


class SetupConfig( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _verbose = False
    _files = None
    _args = None
    _logfile = None


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def setTestArguments( self, argumentsXmlFile ):
        assert os.path.exists( argumentsXmlFile )
        argsListList = list()
        doc = xml.dom.minidom.parse( argumentsXmlFile )
        groups = doc.getElementsByTagName( 'ArgumentGroup' )

        for eachGroup in groups:
            args = eachGroup.getElementsByTagName( 'arg' )
            l = list()

            for eachArg in args:
                try:
                    l.append( eachArg.firstChild.data )
                except AttributeError:
                    l.append( '' )

            argsListList.append( l )

        self._args = list()
        for args in product( *argsListList ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '
            self._args.append( argStr )


    def getTestArguments( self ):
        return self._args


    def setTestFiles( self, fileOrPath, recurse ):
        # Format the path argument slashes
        fileOrPath = os.path.abspath( fileOrPath )

        # Just see if this even exists
        assert os.path.exists( fileOrPath )

        # If this is a file, then just return it as a list
        if( os.path.isfile( fileOrPath ) == True ):
            self._files = [fileOrPath]

        else:
            # Otherwise this is a directory, search for the *.lus files and
            # build a list of the files.
            l = list()
            for filename in self._walk( fileOrPath, recurse, '*.lus' ):
                l.append( filename )

            self._files = l


    def getTestFiles( self ):
        return self._files

    def getLogFile( self ):
        return self._logfile

    def setLogFile( self, fname ):
        self._logfile = fname

    def setVerbose( self, TorF ):
        self._verbose = TorF

    def isVerbose( self ):
        return self._verbose


    def _walk( self, root = '.', recurse = True, pattern = '*' ):
        '''
        Private Function:
        
        Arguments:
        root - the top folder path to walk through
        recurse - if True will go through sub-folders
        pattern - file extension to look for (i.e. *.c)
        
        Description:
        Generator for walking a directory tree.
        Starts at specified root folder, returning files
        that match our pattern. Optionally will also
        recurse through sub-folders.
        '''
        for path, subdirs, files in os.walk( root ):
            for name in files:
                if fnmatch.fnmatch( name, pattern ):
                    yield os.path.join( path, name )
            if not recurse:
                break





class TestConfig( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _fileList = None
    _fileCount = None
    _argsList = None
    _argCount = None


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def setFiles( self, fileList ):
        self._fileList = fileList
        self._fileCount = len( fileList )
        GuiIF().setFileCount( self._fileCount )


    def popFile( self ):
        f = self._fileList.pop()
        GuiIF().setFileUnderTest( f )
        GuiIF().setFileCount( self._fileCount )
        return f


    def fileCount( self ):
        return self._fileCount


    def setArguments( self, argumentsList ):
        self._argsList = argumentsList
        self._argCount = len( argumentsList )


    def next( self ):
        return self.nextArg()


    def nextArg( self ):
        return ( arg for arg in self._argsList )


    def popArgument( self ):
        arg = self._argsList.pop()
        self._argCount = len( self._argsList )
        GuiIF().setArgUnderTest( arg )
        return arg

    def argCount( self ):
        return self._argCount


