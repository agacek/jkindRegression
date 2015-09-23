
import unittest
import os
from jktest.jkind import JKind
from jktest.results import JKindResult
from jktest.results import ResultList


class TC_XmlRead( unittest.TestCase ):

    def setUp( self ):
        self.testFile = './unit_test/test_files/tc_xml_read.xml'

        # Instantiate the JKind class.
        self.jk = JKind( 'dummy', 'dummy' )

        # Don't actually run JKind, but rather sneak our knonw XML file
        # in through the private read method.
        self.jk._parseXML( self.testFile )


    def tearDown( self ):
        pass


    def testFileExists( self ):
        '''
        First make sure the path is correct for the test file
        '''
        exists = os.path.exists( os.path.abspath( self.testFile ) )
        self.assertTrue( exists, 'File Under Test Exists?' )


    def testResultsLength( self ):
        '''
        Test that the Length of the Results list matches our expectation
        '''
        listLen = len( self.jk._results )
        EXP_LIST_LEN = 5
        self.assertEqual( EXP_LIST_LEN, listLen, "Results List is Length?" )


    def testSuccess( self ):
        '''
        Test that the Properties (Variables) match what we expect
        '''

        # This is a list of JKind Results read from the file
        testlst = self.jk._results

        # Create a specialized results list for testing
        explst = ResultList()

        res = JKindResult( '', '' )
        res['name'] = 'var1'
        res['answer'] = 'valid'
        res['K'] = '0'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var2'
        res['answer'] = 'valid'
        res['K'] = '1'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var3'
        res['answer'] = 'valid'
        res['K'] = '2'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var4'
        res['answer'] = 'valid'
        res['K'] = '3'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var5'
        res['answer'] = 'falsifiable'
        res['K'] = '6'
        explst.append( res )


        self.assertEqual( testlst, explst, 'Test the read and expected lists' )


    def testFail( self ):
        '''
        Test expected to Fail
        '''

        # This is a list of JKind Results read from the file
        testlst = self.jk._results

        # Create a specialized results list for testing
        explst = ResultList()


        # This first name is intentionally incorrect
        res = JKindResult( '', '' )
        res['name'] = 'var'  # << WRONG on purpose
        res['answer'] = 'valid'
        res['K'] = '0'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var2'
        res['answer'] = 'valid'
        res['K'] = '1'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var3'
        res['answer'] = 'valid'
        res['K'] = '2'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var4'
        res['answer'] = 'valid'
        res['K'] = '3'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var5'
        res['answer'] = 'falsifiable'
        res['K'] = '6'
        explst.append( res )

        self.assertNotEqual( testlst, explst, 'Test exepected to fail' )


    def testBadLen( self ):
        '''
        Test that our Results List class can deal with mis-matching count of 
        results.
        '''

        # This is a list of JKind Results read from the file
        testlst = self.jk._results

        # Create a specialized results list for testing
        explst = ResultList()

        # The hand-coded Results are correct, except left out the 'var2' entry
        # to see that the Results list class will detect this.
        res = JKindResult( '', '' )
        res['name'] = 'var1'
        res['answer'] = 'valid'
        res['K'] = '0'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var3'
        res['answer'] = 'valid'
        res['K'] = '2'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var4'
        res['answer'] = 'valid'
        res['K'] = '3'
        explst.append( res )

        res = JKindResult( '', '' )
        res['name'] = 'var5'
        res['answer'] = 'falsifiable'
        res['K'] = '6'
        explst.append( res )

        self.assertNotEqual( testlst, explst, 'Test expected to fail' )

