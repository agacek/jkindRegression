
import unittest
from newtest.config import SetupConfig
from newtest.config import TestConfig
from .testcase import MyTestCase

def runtest():

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
    result = unittest.TextTestRunner( verbosity = 2 ).run( suite )

    print( result )
