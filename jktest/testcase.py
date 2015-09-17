
from .config import TestConfig
import unittest
from jktest.jkind import JKind
from jktest.results import ResultList


class MyTestCase( unittest.TestCase ):

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )

    def setUp( self ):
        self.results = ResultList()
        self.file = TestConfig().popFile()

        for i in range( TestConfig().argCount() ):
            self.results.append( JKind( self.file, TestConfig().popArgument() ).run() )

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

            self.assertTrue( ok, 'Test File: ' + self.file )




