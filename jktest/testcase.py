
import unittest
from jktest.guiIF import GuiIF
from jktest.jkind import JKind
from jktest.results import ResultList


def testCaseFactory( filename, argsList ):

    className = filename
    testargs = list( argsList )
    return type( className, ( __JKTestCase__, ), {'file' : filename, 'args' : testargs} )



class __JKTestCase__( unittest.TestCase ):
    '''
    **Private Class**
    
    Think of this as an Abstract Base Class (though this concept doesn't
    exist in Python).
    
    '''

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )


    def setUp( self ):
        self.results = ResultList()
        self.exceptions = list()
        GuiIF().setFileUnderTest( self.file )

        # Print test header for nicer output formatting
        print( '\n**********************************************' )
        print( 'BEGIN TEST OF: ' + str( self.file ) )

        for arg in self.args:
            GuiIF().setArgUnderTest( arg )
            jk = JKind( self.file, arg )
            jk.run()

            # Do not append None-type result returns
            if( jk.getResults() != None ):
                self.results.append( jk.getResults() )

            # Ok, and desirable to append None-type exception returns
            self.exceptions.append( jk.getException() )


    def tearDown( self ):
        print( '\nEND TEST OF ' + str( self.file ) )


    def test_result( self ):

        # First test the JKind Results
        resultsList = self.results.copy()
        controlList = resultsList.pop()
        controlList.sort()

        for each in resultsList:

            with self.subTest( 'subtest results' ):

                each.sort()
                ok = ( controlList == each )
                GuiIF().logSubTestResult( ok )
                self.assertTrue( ok, 'Test File: ' + self.file )

        # Now check for any Java exceptions that may have occurred
        for excp in self.exceptions:

            with self.subTest( 'subtest exceptions' ):
                try:
                    msg = 'Exception Occurred-> {} {}'.format( excp.text, excp.args )
                except AttributeError:
                    msg = 'Exception Occurrred'
                self.assertIsNone( excp, msg )
