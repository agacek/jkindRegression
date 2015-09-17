import os
import argparse
from jktest.testsuite import runsuite
from jktest.config import SetupConfig
try:
    from gui.launch import launchGUI
except:
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = 'JKind regression test' )

    # Mandatory-ish arguments. User must specify either -files (with file or path), or
    # specify -gui to launch the GUI, or the may specify both to load the files and
    # launch the GUI.
    parser.add_argument( '-files', help = 'Filename to run or Directory to search for *.lus files' )
    parser.add_argument( '--gui',
                         action = 'store_true',
                         help = 'Display GUI' )

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

    # Parse the files to test
    SetupConfig().setTestFiles( args.files, args.recur )

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
