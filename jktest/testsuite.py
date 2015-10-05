'''
This module contains the Test Suite.

'''

import os
import sys
import unittest
from jktest.config import SetupConfig
from jktest.guiIF import GuiIF
from jktest.testcase import testCaseFactory


DEFAULT_ARGUMENT_FILE = 'default_args.xml'


def runsuite( verbose = True ):
    '''
    **Public Function**
    
    This function executes the test suite. Performs the following:
    
    - If specified, opens the log file. Otherwise defaults stdout to console.
    - Loads the arguments xml file, either specified or default.
    - Uses the test case factory to dynamically create the test case classes,
      loaded with the filename and the argument sets.
    - Executes the test suite
    
    :param verbose: flag to increase verbosity
    :type verbose: bool
    
    :return: flag whether the test was successful or not
    :rtype: bool
    
    '''

    # Try to open the log file, if it even exists. Try to redirect the i/o
    # to the log file.
    try:
        logfile = open( SetupConfig().getLogFile(), 'w' )
        sys.stdout = logfile
    except:
        logfile = None
        sys.stdout = sys.__stdout__

    # If a test arguments XML file wasn't specified, then set the default.
    if ( SetupConfig().getTestArguments() == None ):
        assert os.path.exists( DEFAULT_ARGUMENT_FILE )
        SetupConfig().setTestArguments( DEFAULT_ARGUMENT_FILE )

    # Build a Test Suite made of the Generic test functions. The specific file and
    # arguments run in the tests are determined at execution time.
    testCases = []
    loader = unittest.TestLoader()

    GuiIF().setFileCount( len( SetupConfig().getTestFiles() ) )

    for filename in SetupConfig().getTestFiles():
        testClass = testCaseFactory( filename, SetupConfig().getTestArguments() )
        testCases.append( loader.loadTestsFromTestCase( testClass ) )

    suite = unittest.TestSuite( testCases )
    result = unittest.TextTestRunner( verbosity = 2, stream = logfile ).run( suite )

    if( verbose == True ):
        print( '\n\n\n*****************************************' )
        print( 'Overall TestSuite Result:' )
        print( result )

    # Try to close the log file
    try:
        logfile.close()
    except:
        pass

    # Try to tell the GUI that all is finished
    GuiIF().signalSuiteComplete()

    # Return an overall boolean pass/fail. Typically used for the self unittests.
    return result.wasSuccessful()

