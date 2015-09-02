
from itertools import product
from jkind.jkind_exec import jkind_exec


def go( filename ):

    # If just a single file as a string, then convert to a list
    if( isinstance( filename, str ) == True ):
        filename = [filename]

    # Iterate through the filenames as top level for the Tests
    for thefile in filename:

        # TODO: This needs to come from an xml config file
        argLists = [
                    ['-solver yices', '-solver smtinterpol', '-solver cvc4'],
                    ['-no_k_induction', '-pdr_max 0']
                ]

        for args in product( *argLists ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '

            # Run jkind
            jkind_exec( thefile, argStr )
