
from itertools import product
from jkind.jkind_exec import jkind_exec
from data import FileTest
from data import FileSuite
from .test_config import getArguments

def go( filename ):

    # If just a single file as a string, then convert to a list
    if( isinstance( filename, str ) == True ):
        filename = [filename]

    # Iterate through the filenames as top level for the Tests
    for thefile in filename:

        suite = FileSuite()

        # Read the arguments from the test configuration xml file.
        # A list-of-lists will be returned. Each sub-list is a series of
        # related arguments to be individually used in the iterations.
        argLists = getArguments()

        # TODO: This needs to come from an xml config file
        # argLists = [
        #            ['-solver yices', '-solver smtinterpol', '-solver cvc4'],
        #            ['', '-no_k_induction', '-pdr_max 0']
        #        ]

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
        print( s )
