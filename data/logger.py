
import os
from .internaldata import InternalData


class Logger( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define the shared data
    _file = None
    _count = 0
    _fileIdx = 0


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def open( self ):
        # Open the log file
        filename = os.path.join( InternalData().getOutputDir(), 'jkind_test.log' )
        self._file = open( filename, 'w' )
        self._count = 0
        self._fileIdx = 0


    def close( self ):
        self._file.close()


    def fileCount( self, count = None ):
        if( count != None ):
            self._count = count
        return self._count


    def incrementFileIdx( self ):
        self._fileIdx += 1


    def log( self, logstr ):

        print( logstr )

        try:
            if( logstr.endswith( '\n' ) == False ):
                logstr += '\n'
            self._file.write( logstr )
        except:
            pass
