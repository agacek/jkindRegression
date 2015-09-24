
import os
import unittest
from jktest.jkind import JKind


class TC_XmlOrder( unittest.TestCase ):

    def setUp( self ):
        self.testFile1 = './unit_test/test_files/order_1.xml'
        self.testFile2 = './unit_test/test_files/order_2.xml'

        # Instantiate the JKind classes
        self.jk1 = JKind( 'dummy', 'dummy' )
        self.jk2 = JKind( 'dummy', 'dummy' )

        # Don't actually run JKind, but rather sneak our known XML file
        # in through the private read method.
        self.jk1._parseXML( self.testFile1 )
        self.jk2._parseXML( self.testFile2 )


    def tearDown( self ):
        pass


    def testFileExists( self ):
        '''
        First make sure the path is correct for the test files
        '''
        exists = os.path.exists( os.path.abspath( self.testFile1 ) )
        self.assertTrue( exists, 'File Under Test 1 Exists?' )

        exists = os.path.exists( os.path.abspath( self.testFile2 ) )
        self.assertTrue( exists, 'File Under Test 2 Exists?' )


    def testResultsLength( self ):
        '''
        Test that the Length of the Results list matches our expectation
        '''
        EXP_LIST_LEN = 4

        listLen = len( self.jk1._results )
        self.assertEqual( EXP_LIST_LEN, listLen, "Results List is Length?" )

        listLen = len( self.jk2._results )
        self.assertEqual( EXP_LIST_LEN, listLen, "Results List is Length?" )


    def testFail( self ):
        testlst1 = self.jk1._results
        testlst2 = self.jk2._results

        ok = ( testlst1 == testlst2 )

        self.assertFalse( ok, 'Results should not be equal' )

        # The second and third Properties in the XML files are out of order
        # and should've generated a failure string. Check that this is true.
        a = testlst1[1].failures()
        self.assertEqual( len( a ), 1, 'Second Property should have failure string' )

        b = testlst1[2].failures()
        self.assertEqual( len( b ), 1, 'Third Property should have failure string' )


    def testSuccess( self ):
        '''
        Test that the Properties (Variables) match what we expect.
        The order of the Properties are intentionally out of order in the XML file.
        This checks that our ResultsList can be sorted prior to equality testing.
        '''

        # This is a list of JKind Results read from the file
        testlst1 = self.jk1._results.copy()
        testlst2 = self.jk2._results.copy()

        testlst1.sort()
        testlst2.sort()

        ok = ( testlst1 == testlst2 )

        for jkr in testlst1:
            for line in jkr.failures():
                print( line )

        self.assertTrue( ok, 'Test the results' )

