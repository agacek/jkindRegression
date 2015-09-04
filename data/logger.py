
import os
from .internaldata import InternalData


class Logger( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define the shared data
    _file = None



    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def open( self ):
        # Open the log file
        filename = os.path.join( InternalData().getOutputDir(), 'jkind_test.log' )
        self._file = open( filename, 'w' )


    def close( self ):
        self._file.close()


    def log( self, logstr ):

        print( logstr )

        if( logstr.endswith( '\n' ) == False ):
            logstr += '\n'
        self._file.write( logstr )
