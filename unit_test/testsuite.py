import sys
import unittest

from unit_test.tc_pre_lus import TC_PreFile
from unit_test.tc_tuple_lus import TC_TupleFile
from test_runner.logger import Logger



class TestSuite():

    def execute( self, verbose = True ):

        loader = unittest.TestLoader()
        testCases = []

        testCases.append( loader.loadTestsFromTestCase( TC_PreFile ) )
        testCases.append( loader.loadTestsFromTestCase( TC_TupleFile ) )

        Logger().enableStdOut( verbose )
        suite = unittest.TestSuite( testCases )

        result = unittest.TextTestRunner( verbosity = 2 ).run( suite )
        Logger().enableStdOut( True )

        print( result )
