
from itertools import product
from jkind.jkind_exec import jkind_exec
from data.logger import Logger
from data.testdefns import FileTest
from data.testdefns import FileSuite

from test_runner._test_config import getArguments

def runtest( filenames ):

    # If just a single file as a string, then convert to a list
    if( isinstance( filenames, str ) == True ):
        filenames = [filenames]

    # Open the logger
    Logger().open()

    # Iterate through the filenames as top level for the Tests
    for thefile in filenames:

        suite = FileSuite( thefile )

        # Read the arguments from the test configuration xml file.
        # A list-of-lists will be returned. Each sub-list is a series of
        # related arguments to be individually used in the iterations.
        argLists = getArguments()

        for args in product( *argLists ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '

            # Run jkind
            resultList = jkind_exec( thefile, argStr )

            # Compile the results of this run and add it to the
            # file test suite.
            fileTest = FileTest( thefile, argStr, resultList )
            suite.addFileTest( fileTest )

        # All done iterating through the arguments.
        # Now let's validate the results
        suite.validate()
        s = suite.toString()
        Logger().log( s )

    # Close the logger
    Logger().close()