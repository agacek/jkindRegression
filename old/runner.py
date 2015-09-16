
from .logger import Logger
from my_os.dirs import parseFileArg
from .test_case import TestCase
from .internaldata import SetupConfig

def runtest():

    # Get the path and the recursion flag from the command line arguments
    path = SetupConfig().getTestPath()
    recurse = SetupConfig().getRecurseFlag()

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
    for theFile in filenames:

        tc = TestCase( theFile )
        result = tc.runTest()
        Logger().logResult( result, theFile )

    # Check the Logger for the Summary
    ok = Logger().summary()

    # Close the logger
    Logger().close()

    # Return the overall pass/fail flag.
    return ok
