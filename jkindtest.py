import os
import argparse
from jktest.runner import runtest
from jktest.config import SetupConfig
try:
    from gui.launch import launchGUI
except:
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = 'JKind regression test' )

    # Mandatory Positional arguments
    parser.add_argument( 'files', help = 'Filename to run or Directory to search for *.lus files' )

    # Optional arguments
    parser.add_argument( '-argfile', help = 'Alternate Config XML file <default is test_config.xml>' )
    parser.add_argument( '-logfile', help = 'Log to file, supply filename' )


    # Flags
    parser.add_argument( '-recur',
                        action = 'store_true',
                        help = 'Flag to look for files in subdirectories when Directory is specified' )
    parser.add_argument( '-gui',
                         action = 'store_true',
                         help = 'Display GUI' )

    args = parser.parse_args()

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
        runtest()
