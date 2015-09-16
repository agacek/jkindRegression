
import os
import unittest


class TC_TupleFile( unittest.TestCase ):

    def setUp( self ):
        self.testFile = './unit_test/test_files/tuple.lus'

    def tearDown( self ):
        pass


    def testFileExists( self ):
        '''
        First make sure the path is correct for the tuple.lus file
        '''
        exists = os.path.exists( os.path.abspath( self.testFile ) )
        self.assertTrue( exists, 'File Under Test Exists?' )


    def testResult( self ):
        '''
        Run the pre.lus file. Expect this to fail
        '''
        # SetupConfig().setTestPath( self.testFile )
        # rv = runtest()
        # self.assertFalse( rv, 'tuple.lus file Fails?' )

