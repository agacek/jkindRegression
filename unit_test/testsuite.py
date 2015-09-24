
import unittest

from unit_test.tc_pre_lus import TC_PreFile
from unit_test.tc_tuple_lus import TC_TupleFile
from unit_test.tc_xml_read import TC_XmlRead
from unit_test.tc_xml_order import TC_XmlOrder


def runTestSuite():

    loader = unittest.TestLoader()
    testCases = []

    testCases.append( loader.loadTestsFromTestCase( TC_PreFile ) )
    testCases.append( loader.loadTestsFromTestCase( TC_TupleFile ) )
    testCases.append( loader.loadTestsFromTestCase( TC_XmlRead ) )
    testCases.append( loader.loadTestsFromTestCase( TC_XmlOrder ) )

    suite = unittest.TestSuite( testCases )

    result = unittest.TextTestRunner( verbosity = 2 ).run( suite )

    print( '\n\n\n*****************************************' )
    print( 'Overall TestSuite Result:' )
    print( result )
