'''
This module contains utilities for post-processing the output log

'''

import io
import os
import shutil
import subprocess
import sys
from jktest.config import SetupConfig


class Tee( object ):
    '''
    **Public Class**
    
    Instantiations of this class are used to set the sys.stdout.
    By specifying multiple files, or sys.__stdout__, can redirect stdout to
    multiple targets.
    
    Typical usage is to specify a file and the sys.__stdout__ to write to both
    a file and the console.
    
    f = open('somefile.log', 'w')
    sys.stdout = Tee( sys.__stdout__, f )
    
    '''
    def __init__( self, *files ):
        '''
        **Constructor**
        
        :param \*files: any number of stdout objects to write output to
        :type \*files: <_io.TextIOWrapper>
        '''
        self.files = files


    def write( self, obj ):
        '''
        **Public Method**
        
        Implementation of the TextIOWrapper write method. Typically not 
        explicitly called, but rather provides the method for stdout to access.
        
        :param obj: Any object type that implements write() for stdout
        :return: n/a:
        
        '''
        for f in self.files:
            f.write( obj )
            f.flush()  # If you want the output to be visible immediately


    def flush( self ) :
        '''
        **Public Method**
        
        Implementation of the TextIOWrapper flush method. Typically not
        explicitly called, but rather provides the method for stdout to access.
        
        :return: n/a:
        
        '''
        for f in self.files:
            f.flush()


    def closeFiles( self ):
        '''
        **Public Method**
        
        This method attempts to close any files that may have been opened.
        Catches and passes all exceptions.
        
        :return: n/a:
        
        '''

        for f in self.files:
            try:
                f.close()
            except:
                pass


def openLog():
    '''
    **Public Function**

    Opens the log file, if one was specified. If so will direct the stdio
    to both the file and to the console. If no file, then just to the
    console.
    
    :return: The opened file if available otherwise None
    :rtype: file *or* None
    
    '''
    try:
        logfile = open( SetupConfig().getLogFile(), 'w' )
        sys.stdout = Tee( sys.__stdout__, logfile )
    except:
        logfile = None
        sys.stdout = sys.__stdout__
    return logfile


def closeLog():
    '''
    **Public Function**
    
    Closes the log file, if it were opened. Restores the stdio back
    to the console.
    
    :return: n/a:
    
    '''
    try:
        sys.stdout.closeFiles()
    except:
        pass
    sys.stdout = sys.__stdout__


def jkindVersion():
    '''
    **Public Function**
    
    Gets the jkind version string. Asserts if the following solvers aren't
    found: yices, yices2, cvc4, z3, smtinterpol.
    
    :rtype: string
    
    '''
    jkindJar = SetupConfig().getJkindFile()
    javaPath = SetupConfig().getJava()

    if( javaPath == None ):
        java = 'java'
    else:
        java = javaPath

    if( jkindJar == None ):
        jkind = 'jkind --version'
    else:
        jkind = '{} -jar {} -jkind --version '.format( java, jkindJar )

    proc = subprocess.Popen( jkind,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             shell = True )
    ( out, err ) = proc.communicate()

    ver = out.decode()

    assert ver.find( 'yices,' ) > 0, 'Assertion Error: yices solver not detected'
    assert ver.find( 'yices2' ) > 0, 'Assertion Error: yices2 solver not detected'
    assert ver.find( 'z3' ) > 0, 'Assertion Error: z3 solver not detected'
    assert ver.find( 'cvc4' ) > 0, 'Assertion Error: cvc4 solver not detected'
    assert ver.find( 'smtinterpol' ) > 0, 'Assertion Error: smtinterpol solver not detected'

    return ver


def splitLog( logfile ):
    '''
    **Public Function**
    
    Given a log file, this function will parse and write out the individual
    lustre results to a like-named text file. These files are saved in a
    sub-folder with the same name as the original log file.
    
    :param logfile: Fully qualified filename of the log file to parse.
    :type logfile: str
    
    :return: n/a:

    '''

    # First off just make sure this logfile exists. If not assert.
    assert os.path.exists( logfile ) == True


    # Get the begin and end tag strings from the configuration. These are
    # later used to determine individual lustre file results in the
    # log file.
    beginTag = SetupConfig().getBeginTestTag()
    endTag = SetupConfig().getEndTestTag()

    # Create the path name of the output subfolder based upon the log file
    # name. Then try to delete it so we don't have any stale file left over.
    # After deleting, recreate the empty folder.
    path = os.path.dirname( logfile )
    path = os.path.join( path, os.path.basename( logfile ).split( '.' )[0] )
    path = os.path.abspath( path )

    try:
        shutil.rmtree( path )
    except FileNotFoundError:
        pass

    # Should always be able to create this, but periodically getting a
    # Windows Permission exception.
    try:
        os.makedirs( path )
    except PermissionError:
        pass

    # Open the log file and read all the lines in to a list.
    with open( logfile, mode = 'r' ) as f:
        log = f.readlines()

    # Iterate through all the log file lines. If a begin tag is found will
    # open a new log file in the subfolder, name based upon the lustre file.
    # If an end tag is found will close the file. In between will write the
    # lines to the lustre log file.
    for line in log:
        if( line.startswith( beginTag ) == True ):
            fname = ( line.split( beginTag )[1] ).strip()
            fname += '.log'
            fname = os.path.basename( fname )
            fname = os.path.abspath( os.path.join( path, fname ) )
            f = io.open( fname, 'w', newline = '' )

        try:
            f.write( line )
        except:
            pass

        if( line.startswith( endTag ) == True ):
            f.close()
