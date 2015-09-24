import os
import fnmatch
import xml.dom.minidom
from itertools import product


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
        if( isinstance( self._args, list ) == True ):
            return list( self._args )
        else:
            return None


    def setTestFiles( self, fileOrPath, recurse ):

        # Test to see if this is list-type. If so assume that it's a list of filenames.
        # We DO NOT support a list of directories.
        if( isinstance( fileOrPath, list ) == True ):
            self._files = list( fileOrPath )

            assert len( fileOrPath ) > 0  # Make sure this insn't an empty list

            # Test that the files exist
            for each in self._files:
                assert os.path.exists( each ), 'User specified file/path does not exist'

        # Otherwise we believe we've received either a single file name or a
        # directory for us to search for *.lus files.
        else:
            # Make sure this even exists
            assert os.path.exists( fileOrPath ), 'User specified file/path does not exist'

            # Format the path argument slashes
            fileOrPath = os.path.abspath( fileOrPath )

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
        if( isinstance( self._files, list ) == True ):
            return list( self._files )
        else:
            return None


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
