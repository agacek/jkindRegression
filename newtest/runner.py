
import unittest
from newtest.configdata import ConfigData
from newtest.testdata import TestData
from .testcase import mySetUp
from .testcase import myTearDown
from .testcase import testFunction


def runtest():

    # Transfer Configuration Data to the Test Specific Data store
    TestData().setFiles( ConfigData().getTestFiles() )
    TestData().setArguments( ConfigData().getTestArguments() )

    # Build a Test Suite made of the Generic test functions. The specific file and
    # arguments run in the tests are determined at execution time.
    testCases = []
    # for each in fileList:
    for i in range( TestData().fileCount() ):
        tc = unittest.FunctionTestCase( testFunction, mySetUp, myTearDown, description = 'Generic Test Case Function' )
        testCases.append( tc )

    suite = unittest.TestSuite( testCases )
    result = unittest.TextTestRunner( verbosity = 2 ).run( suite )

    print( result )
