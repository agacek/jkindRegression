
import unittest
from jktest.config import TestConfig
from jktest.jkind import JKind
from jktest.results import ResultList

class TestCase( unittest.TestCase ):
    def assertTrue( self, expr, msg = None ):
        super( TestCase, self ).assertTrue( expr, msg )



class JKTestCase( unittest.TestCase ):
# class JKTestCase( TestCase ):

    def __init__( self, methodName = 'runTest' ):
        unittest.TestCase.__init__( self, methodName = methodName )

    def setUp( self ):
        self.results = ResultList()
        self.file = TestConfig().popFile()

        for arg in TestConfig().nextArg():
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

            self.assertTrue( ok, 'Test File: ' + self.file )






