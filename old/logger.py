
import os
import time
from .events import Events
from .events import EventTypes
from .internaldata import SetupConfig



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
    _failedFileList = None
    _startTime = 0
    _endTime = 0
    _enableStdOut = True


    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def open( self ):
        # Open the log file
        filename = os.path.join( SetupConfig().getOutputDir(), 'jkind_test.log' )
        self._logfile = open( filename, 'w' )
        self._count = 0
        self._fileIdx = 0
        self._fileUnderTest = ''
        self._argumentUnderTest = ''
        self._passCount = 0
        self._failCount = 0
        self._failedFileList = list()
        self._startTime = time.time()



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


    def enableStdOut( self, TorF ):
        self._enableStdOut = TorF


    def logFile( self, filename ):
        self._fileIdx += 1
        s = '\n\n-----------------------------------------\n'
        s += 'File ' + str( self._fileIdx ) + '/' + str( self.fileCount() )
        s += ': ' + filename
        self.logString( s )

        self._fileUnderTest = filename
        Events().update( EventTypes.GUI_UPDATE )


    def logArguments( self, args ):
        self.logString( args )
        self._argumentUnderTest = args
        Events().update( EventTypes.GUI_UPDATE )


    def logResult( self, resultBool, filename ):
        if( resultBool == True ):
            self._passCount += 1
            s = 'PASS'
        else:
            self._failCount += 1
            self._failedFileList.append( filename )
            s = 'FAIL'
        self.logString( s )
        Events().update( EventTypes.GUI_UPDATE )


    def logString( self, logstr ):

        if( self._enableStdOut == True ):
            print( logstr )

        try:
            if( logstr.endswith( '\n' ) == False ):
                logstr += '\n'
            self._logfile.write( logstr )
        except:
            pass


    def summary( self ):

        self.logString( '\n\nTEST SUMMARY:' )

        # Find the rough execution time
        self._endTime = time.time()
        secs = int( self._endTime - self._startTime )
        s = str( self.fileCount() ) + ' files executed in ' + str( secs ) + ' seconds'
        self.logString( s )

        # Pass/Fail count
        self.logString( 'PASS: ' + str( self.passCount() ) )
        self.logString( 'FAIL: ' + str( self.failCount() ) )

        # Print any files that may have failed
        if( len( self._failedFileList ) > 0 ):
            self.logString( '\nFAILED FILES:' )
            for each in self._failedFileList:
                self.logString( each )

        # Give an overall pass/fail indicator
        if( self.failCount() == 0 ):
            return True
        else:
            return False






