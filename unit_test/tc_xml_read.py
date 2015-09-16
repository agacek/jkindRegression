
import unittest
import os


class TC_XmlRead( unittest.TestCase ):

    def setUp( self ):
        self.testFile = './unit_test/test_files/testXml1.xml'


    def tearDown( self ):
        pass


    def testFileExists( self ):
        '''
        First make sure the path is correct for the test file
        '''
        exists = os.path.exists( os.path.abspath( self.testFile ) )
        self.assertTrue( exists, 'File Under Test Exists?' )


    def testResult( self ):
        '''
        Read the Properties from the XML File and validate
        '''
        pass
