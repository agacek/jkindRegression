import os
import argparse
from test_runner.runner import runtest
from test_runner.internaldata import InternalData
from gui.launch import launchGUI



if __name__ == '__main__':

    # name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    # checkEnvVars()
    # go( name )

    parser = argparse.ArgumentParser( description = 'JKind regression test' )

    # Mandatory Positional arguments
    parser.add_argument( 'files', help = 'Filename to run or Directory to search for *.lus files' )

    # Optional arguments
    parser.add_argument( '-config', help = 'Alternate Config XML file <default is test_config.xml>' )
    parser.add_argument( '-dest', help = 'Alternate log destination <default is ./output>' )


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


    # Add the path and the recursion flag to our Internal Data
    InternalData().setTestPath( args.files )
    InternalData().setRecurseFlag( args.recur )

    # Check if an alternate xml configuration file was specified.
    if( args.config ):
        assert os.path.exists( args.config )
        InternalData().setXmlConfigFile( args.config )

    # Check if an alternate log destination was specified
    if( args.dest ):
        assert os.path.exists( args.dest )
        InternalData().setOutputDir( args.dest )

    # Verbose?
    if( args.verbose ):
        InternalData().setVerbose( True )
    else:
        InternalData().setVerbose( False )


    # Launch either the command line or GUI
    if( args.gui ):
        launchGUI()
    else:
        runtest()
