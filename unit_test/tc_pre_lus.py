
import unittest
import os
from jktest.config import SetupConfig
from jktest.testsuite import runsuite


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
        SetupConfig().setTestFiles( self.testFile, False )

        try:
            ok = runsuite( verbose = False )
        except:
            pass

        self.assertTrue( ok, 'pre.lus file Passes?' )
