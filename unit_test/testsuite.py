
import unittest

# from unit_test.tc_pre_lus import TC_PreFile
# from unit_test.tc_tuple_lus import TC_TupleFile
from .tc_jkind_result import TC_JKind_Result



class TestSuite():

    def execute( self, verbose = True ):

        loader = unittest.TestLoader()
        testCases = []

        # testCases.append( loader.loadTestsFromTestCase( TC_PreFile ) )
        # testCases.append( loader.loadTestsFromTestCase( TC_TupleFile ) )
        testCases.append( loader.loadTestsFromTestCase( TC_JKind_Result ) )

        suite = unittest.TestSuite( testCases )

        result = unittest.TextTestRunner( verbosity = 2 ).run( suite )

        print( result )
