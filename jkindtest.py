import os
import argparse
from newtest.runner import runtest
from newtest.config import SetupConfig
# from gui.launch import launchGUI


DEFAULT_ARGUMENT_FILE = 'test_arguments.xml'


if __name__ == '__main__':

    # name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    # checkEnvVars()
    # go( name )

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
    parser.add_argument( '-verbose',
                         action = 'store_true',
                         help = 'Enable verbose log and shell outputs' )
    parser.add_argument( '-gui',
                         action = 'store_true',
                         help = 'Display GUI' )

    args = parser.parse_args()


    # Parse the files to test
    SetupConfig().setTestFiles( args.files, args.recur )

    # Check if an alternate xml configuration file was specified.
    if( args.argfile ):
        assert os.path.exists( os.path.dirname( args.argfile ) )
        SetupConfig().setTestArguments( args.argfile )
    else:
        SetupConfig().setTestArguments( DEFAULT_ARGUMENT_FILE )

    # Check if an alternate log destination was specified
    if( args.logfile ):
        assert os.path.exists( os.path.dirname( args.logfile ) )
        SetupConfig().setLogFile( args.logfile )

    # Verbose?
    if( args.verbose ):
        SetupConfig().setVerbose( True )
    else:
        SetupConfig().setVerbose( False )


    # Launch either the command line or GUI
    if( args.gui ):
        # launchGUI()
        pass
    else:
        runtest()
