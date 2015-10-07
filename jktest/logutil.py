'''
This module contains utilities for post-processing the output log

'''

import io
import os
from .config import SetupConfig


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

    # Get the begin and end tag strings from the configuration. These are
    # later used to determine individual lustre file results in the
    # log file.
    beginTag = SetupConfig().getBeginTestTag()
    endTag = SetupConfig().getEndTestTag()

    # Create the path name of the output subfolder based upon the log file
    # name. Then try to create it, catching and passing any exceptions.
    path = os.path.dirname( logfile )
    path = os.path.join( path, os.path.basename( logfile ).split( '.' )[0] )

    try:
        os.mkdir( path )
    except FileExistsError:
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
