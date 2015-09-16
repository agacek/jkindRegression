import sys
import unittest

# from unit_test.tc_pre_lus import TC_PreFile
# from unit_test.tc_tuple_lus import TC_TupleFile



class TestSuite():

    def execute( self, verbose = True ):

        loader = unittest.TestLoader()
        testCases = []

        # testCases.append( loader.loadTestsFromTestCase( TC_PreFile ) )
        # testCases.append( loader.loadTestsFromTestCase( TC_TupleFile ) )

        suite = unittest.TestSuite( testCases )

        result = unittest.TextTestRunner( verbosity = 2 ).run( suite )

        print( result )
