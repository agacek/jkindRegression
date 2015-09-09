
from itertools import product
from ._jkind import jkind_exec
from data.logger import Logger
from data.testdefns import FileSuite
from my_os.dirs import parseFileArg
from test_runner._test_config import getArguments

def runtest( path, recurse ):

    # Check if a specific file was specified or if a directory was specified.
    # This will throw an exception if the file or directory does not exist
    # Check the recursion flag, but will be a don't-care if a file was specified.
    filenames = parseFileArg( path, recurse )

    # If just a single file as a string, then convert to a list
    if( isinstance( filenames, str ) == True ):
        filenames = [filenames]

    # Open the logger and initialize the number of files
    Logger().open()
    Logger().fileCount( len( filenames ) )

    # Iterate through the filenames as top level for the Tests
    for thefile in filenames:

        suite = FileSuite( thefile )

        # Read the arguments from the test configuration xml file.
        # A list-of-lists will be returned. Each sub-list is a series of
        # related arguments to be individually used in the iterations.
        argLists = getArguments()

        # Log the file
        Logger().logFile( thefile )

        for args in product( *argLists ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '

            # Run jkind
            Logger().logArguments( argStr )
            results = jkind_exec( thefile, argStr )

            # Compile the results of this run and add it to the
            # file test suite.
            suite.addFileTest( results )

        # All done iterating through the arguments.
        # Now let's validate the results
        result = suite.validate()
        s = suite.toString()
        Logger().logResult( result, s )

        # Logger().logString( s )

    # Close the logger
    Logger().close()
