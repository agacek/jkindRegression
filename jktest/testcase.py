
import unittest
from jktest.guiIF import GuiIF
from jktest.jkind import JKind
from jktest.results import ResultList


def testCaseFactory( filename, argsList ):

    className = filename
    testargs = list( argsList )
    return type( className, ( __JKTestCase__, ), {'file' : filename, 'args' : testargs} )



class __JKTestCase__( unittest.TestCase ):

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )


    def setUp( self ):
        self.results = ResultList()
        GuiIF().setFileUnderTest( self.file )

        # Print test header for nicer output formatting
        print( '\n**********************************************' )
        print( 'BEGIN TEST OF: ' + str( self.file ) )

        for arg in self.args:
            GuiIF().setArgUnderTest( arg )
            rv = JKind( self.file, arg ).run()
            if( rv != None ):
                self.results.append( rv )


    def tearDown( self ):
        print( '\nEND TEST OF ' + str( self.file ) )


    def test_result( self ):
        resultsList = self.results.copy()
        controlList = resultsList.pop()
        controlList.sort()

        for each in resultsList:

            with self.subTest( 'subtest' ):

                each.sort()
                ok = ( controlList == each )
                GuiIF().logSubTestResult( ok )
                self.assertTrue( ok, 'Test File: ' + self.file )
