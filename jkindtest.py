import os
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

    s = "JKind Regression Test:\n"
    s += "This tool is to serve as a regression test suite for the JKind tool as "
    s += "applied to the *.lustre files.\n"
    s += "General usage of the tool as follows from command line or shell:\n"
    s += "> python jkindtest.py <files> <recurse dir flag> <gui flag> <opt xml file> <opt log file>"
    s += "\nMandatory specification of either -files or --gui flag"
    s += "Other arguments optional"

    parser = argparse.ArgumentParser( description = s )

    # Mandatory-ish arguments. User must specify either -files (with file or path), or
    # specify -gui to launch the GUI, or the may specify both to load the files and
    # launch the GUI.
    parser.add_argument( '-files', help = 'Filename to run or Directory to search for *.lus files. Use with or in lieu of --gui' )
    parser.add_argument( '--gui',
                         action = 'store_true',
                         help = 'Display GUI - may be used with or in lieu of -files' )

    # Optional arguments
    parser.add_argument( '-argfile', help = 'Alternate Config XML file <default is test_config.xml>' )
    parser.add_argument( '-logfile', help = 'Log to file, supply filename' )

    # Optional Flags
    parser.add_argument( '--recur',
                        action = 'store_true',
                        help = 'Flag to look for files in subdirectories when Directory is specified' )

    args = parser.parse_args()

    if not ( args.files or args.gui ):
        parser.error( 'Must specify -files, --gui, or both' )

    # Parse the files to test. If gui was specified without files this is ok.
    # Otherwise re-throw the file(s) not found exception.
    try:
        SetupConfig().setTestFiles( args.files, args.recur )
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

    # Launch either the command line or GUI
    if( args.gui ):
        launchGUI()
    else:
        runsuite()
