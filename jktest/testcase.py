
from .config import TestConfig
import unittest
from .jkind import JKind


class MyTestCase( unittest.TestCase ):

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )

    def setUp( self ):
        self.file = TestConfig().popFile()
        self.args = TestConfig().getArguments()
        self.results = list()

        for arg in self.args:
            self.results.append( JKind( self.file, arg ).run() )

    def tearDown( self ):
        pass

    def test1( self ):
        resultsList = self.results.copy()
        controlList = resultsList.pop()

        for each in resultsList:

            ok = ( controlList == each )
            if( ok == False ):

                for jkr in controlList:
                    for line in ( jkr.failures() ):
                        print( line )


            # msg = 'Test {} Args <{}> <{}>'.format()
            self.assertTrue( ok, 'test equality' )




