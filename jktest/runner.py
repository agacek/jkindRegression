import sys
import unittest
from .config import SetupConfig
from .config import TestConfig
from .testcase import MyTestCase

def runtest():

    # Try to open the log file, if it even exists. Try to redirect the i/o
    # to the log file.
    try:
        logfile = open( SetupConfig().getLogFile(), 'w' )
        sys.stdout = logfile
    except:
        logfile = None

    # Transfer Setup Data to the Test Specific Data store
    TestConfig().setFiles( SetupConfig().getTestFiles() )
    TestConfig().setArguments( SetupConfig().getTestArguments() )

    # Build a Test Suite made of the Generic test functions. The specific file and
    # arguments run in the tests are determined at execution time.
    testCases = []
    loader = unittest.TestLoader()

    for i in range( TestConfig().fileCount() ):
        testCases.append( loader.loadTestsFromTestCase( MyTestCase ) )

    suite = unittest.TestSuite( testCases )
    result = unittest.TextTestRunner( verbosity = 2, stream = logfile ).run( suite )
    print( result )

    # Try to close the log file
    try:
        logfile.close()
    except:
        pass

