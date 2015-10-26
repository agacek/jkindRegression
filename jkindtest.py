'''
This module is the command line entry point for the JKind Regression Test
Suite. For the arguments, see the source code jkindtest.py or execute:

Return Code == 0 for successful test. 
Return Code == 1 if any failure occurred.

$ python jkindtest.py -h

'''

import os
import sys
import argparse
from jktest.config import SetupConfig
from jktest.testsuite import runsuite
try:
    from gui.launch import launchGUI
except:
    pass


if __name__ == '__main__':
    '''
    Main command line entry point in to the JKind Regression test suite.
    '''

    s = "JKind Regression Test Tool: "
    s += "This tool is to serve as a regression test suite for the JKind tool as "
    s += "applied to the desired Lustre files."


    parser = argparse.ArgumentParser( description = s )

    # Mandatory-ish arguments. User must specify either -files (with file or path), or
    # specify -gui to launch the GUI, or the may specify both to load the files and
    # launch the GUI.
    parser.add_argument( '-file', help = 'Filename to run. Must specify this or -dir or --gui' )
    parser.add_argument( '-dir', help = 'Directory to search for *.lus files. Must specify this or -file or --gui' )
    parser.add_argument( '--gui',
                         action = 'store_true',
                         help = 'Display GUI - may be used individually or with all other arguments.' )

    # Optional arguments
    parser.add_argument( '-argfile', help = 'Alternate Config XML file <default is default_args.xml>' )
    parser.add_argument( '-logfile', help = 'Log to file, supply filename.' )
    parser.add_argument( '-jkind', help = 'Alternate JKind jar file to run' )
    parser.add_argument( '-java', help = 'Alternate Java executable to run. If used you must also specify -jar for JKind.' )

    # Optional Flags
    parser.add_argument( '--recur',
                        action = 'store_true',
                        help = 'Flag to look for files in subdirectories when Directory is specified' )

    parser.add_argument( '--quiet',
                         action = 'store_true',
                         help = 'Flag to suppress non-failing warnings or errors' )

    args = parser.parse_args()


    if( args.dir and args.file ):
        parser.error( '-file and -dir are mutually exclusive' )

    if not ( ( args.file or args.dir ) or args.gui ):
        parser.error( 'Must specify -file, -dir, or --gui' )

    # Parse the files to test. If gui was specified without files this is ok.
    # Otherwise re-throw the file(s) not found exception.
    if( args.file ):
        test = args.file
    else:
        test = args.dir
    try:
        SetupConfig().setTestFiles( test, args.recur )
    except Exception as ex:
        if( args.gui ):
            pass
        else:
            raise Exception( ex )

    # Check if an alternate xml configuration file was specified.
    if( args.argfile ):
        assert os.path.exists( args.argfile )
        SetupConfig().setTestArguments( args.argfile )

    # Check if a log file destination was specified
    if( args.logfile ):
        assert os.path.exists( os.path.dirname( args.logfile ) )
        SetupConfig().setLogFile( args.logfile )

    # Check if an alternate JKind jar file was specified
    if( args.jkind ):
        assert os.path.exists( args.jkind )
        SetupConfig().setJkindFile( args.jkind )

    # Check if an alternate Java executable was specified. Note that we must
    # have also specified the JKind path as well if we want to do this.
    if( args.java and not args.jkind ):
        parser.error( 'Must specify -jkind if using -java' )

    if( args.java ):
        assert os.path.exists( args.java )
        SetupConfig().setJava( args.java )

    # Check if the quiet flag was set
    if( args.quiet ):
        SetupConfig().setQuiet( args.quiet )

    # Launch either the command line or GUI
    if( args.gui ):
        ok = launchGUI()
    else:
        ok = runsuite()

    # Use this to exit such that the application status code is returned
    # to the OS. Return code is typically 0 for success, so convert the
    # boolean return values.
    # Windows show by: echo %ERRORLEVEL%
    sys.exit( not int( ok ) )
