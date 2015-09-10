
import os
from data.events import Events
from data.events import EventTypes
from data.internaldata import InternalData



class Logger( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define the shared data
    _file = None
    _count = 0
    _fileIdx = 0
    _fileUnderTest = ''
    _argumentUnderTest = ''
    _passCount = 0
    _failCount = 0


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def open( self ):
        # Open the log file
        filename = os.path.join( InternalData().getOutputDir(), 'jkind_test.log' )
        self._logfile = open( filename, 'w' )
        self._count = 0
        self._fileIdx = 0
        self._fileUnderTest = ''
        self._argumentUnderTest = ''
        self._passCount = 0
        self._failCount = 0


    def close( self ):
        self._logfile.close()
        Events().update( EventTypes.TEST_DONE )


    def fileCount( self, count = None ):
        if( count != None ):
            self._count = count
        return self._count


    def fileIdx( self ):
        return self._fileIdx


    def fileUnderTest( self ):
        return self._fileUnderTest


    def argumentUnderTest( self ):
        return self._argumentUnderTest


    def passCount( self ):
        return self._passCount


    def failCount( self ):
        return self._failCount


    def logFile( self, filename ):
        self._fileIdx += 1
        s = '\n\n***********************************************************\n'
        s += 'File ' + str( self._fileIdx ) + '/' + str( self.fileCount() )
        s += ': ' + filename
        self.logString( s )

        self._fileUnderTest = filename
        Events().update( EventTypes.GUI_UPDATE )


    def logArguments( self, args ):
        self.logString( args )
        self._argumentUnderTest = args
        Events().update( EventTypes.GUI_UPDATE )


    def logResult( self, resultBool, logString = '' ):
        if( resultBool == True ):
            self._passCount += 1
            s = 'PASS'
        else:
            self._failCount += 1
            s = 'FAIL'
        self.logString( s + ': ' + logString )
        Events().update( EventTypes.GUI_UPDATE )


    def logString( self, logstr ):

        print( logstr )

        try:
            if( logstr.endswith( '\n' ) == False ):
                logstr += '\n'
            self._logfile.write( logstr )
        except:
            pass
