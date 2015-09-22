
import unittest
from jktest.config import TestConfig
from jktest.jkind import JKind
from jktest.results import ResultList
from jktest.guiIF import GuiIF


class JKTestCase( unittest.TestCase ):

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )

    def setUp( self ):
        self.results = ResultList()
        self.file = TestConfig().popFile()

        # Print test header for nicer output formatting
        print( '\n**********************************************' )
        print( 'BEGIN TEST OF: ' + str( self.file ) )

        for arg in TestConfig().next():
            self.results.append( JKind( self.file, arg ).run() )

    def tearDown( self ):
        print( '\nEND TEST OF ' + str( self.file ) )

        # print( str( self.wasSuccessful() ) )



    def test_result( self ):
        resultsList = self.results.copy()
        controlList = resultsList.pop()

        for each in resultsList:

            ok = ( controlList == each )
            GuiIF().logTestResult( ok )
            if( ok == False ):
                for jkr in controlList:
                    for line in ( jkr.failures() ):
                        print( line )

            self.assertTrue( ok, 'Test File: ' + self.file )






