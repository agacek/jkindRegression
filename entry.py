import os
import argparse
from test_runner.runner import runtest
from my_os.dirs import parseFileArg
from data.internaldata import InternalData
# from my_os.env_vars import checkEnvVars



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

    args = parser.parse_args()


    # Check if an alternate xml configuration file was specified.
    if( args.config ):
        assert os.path.exists( args.config )
        InternalData().setXmlConfigFile( args.config )

    # Check if an alternate log destination was specified
    if( args.dest ):
        assert os.path.exists( args.dest )
        InternalData().setOutputDir( args.dest )

    # Check if a specific file was specified or if a directory was specified.
    # This will throw an exception if the file or directory does not exist
    # Check the recursion flag, but will be a don't-care if a file was specified.
    testfiles = parseFileArg( args.files, args.recur )

    runtest( testfiles )
