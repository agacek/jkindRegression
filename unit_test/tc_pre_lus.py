
import unittest
import os
from test_runner.runner import runtest
from test_runner.internaldata import SetupConfig


class TC_PreFile( unittest.TestCase ):

    def setUp( self ):
        self.testFile = './unit_test/test_files/pre.lus'

    def tearDown( self ):
        pass


    def testFileExists( self ):
        '''
        First make sure the path is correct for the pre.lus file
        '''
        exists = os.path.exists( os.path.abspath( self.testFile ) )
        self.assertTrue( exists, 'File Under Test Exists?' )


    def testResult( self ):
        '''
        Run the pre.lus file. Expect this to pass
        '''
        SetupConfig().setTestPath( self.testFile )
        rv = runtest()
        self.assertTrue( rv, 'pre.lus file Passes?' )
