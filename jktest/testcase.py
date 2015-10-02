
import unittest
from jktest.guiIF import GuiIF
from jktest.jkind import JKind
from jktest.results import ResultList


def testCaseFactory( filename, argsList ):
    '''
    **Public Function**
    
    This is a class factory, returning a class definition sub-classed from 
    the JKTestCase "Abstract" Base Class. The arguments to this function
    are added to the class definition by adding to the __dict__.
    
    This class factory is the magic that allows us to define Test Cases
    for all the file and argument combinations and still only having to 
    write a single unittest.TestCase.
    
    :param filename: The qualified filename to run with JKind
    :type filename: str
    :param argsList: The list of all the possible arugment strings to run
    :type argsList: list[str, str, ...]
    
    '''

    className = filename
    testargs = list( argsList )
    return type( className, ( _JKTestCase, ), {'file' : filename, 'args' : testargs} )



class _JKTestCase( unittest.TestCase ):
    '''
    **Private Class**
    
    Think of this as an Abstract Base Class (though this concept doesn't
    exist in Python).
    
    This is the one-and-only test case explicity written for this test suite.
    The class factory sub-classes this and adds the filename and arguments
    to dynamically create the multitude of test cases added to the
    unittest.TestSuite for execution.
    
    '''

    def __init__( self, methodName = 'runTest' ):
        '''
        **Constructor**
        
        Calls the TestCase super constructor. Passes along the 
        methodName argument.
        
        :param methodName: Defaults to "runTest". Typically not specified
                           and letting the default take precedence.
        :type methodName: runner method
        
        '''
        unittest.TestCase.__init__( self, methodName = methodName )


    def setUp( self ):
        '''
        **Public Method**
        
        The execution of the various JKind permutations are actually
        executed here. The results are stashed away in the internal
        results and exceptions data members for testing later.
        
        '''
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
        '''
        **Public Method**
        
        Just prints to stdout that the test is done. No other action.
        
        '''
        print( '\nEND TEST OF ' + str( self.file ) )


    def test_result( self ):
        '''
        **Public Method**
        
        This is where the test assertions for the results and exceptions are
        made.
        
        Iterates through the results of the JKind runs and tests that the 
        results of the individual runs per file do not change based on the
        differing arguments. 
        
        Also checks if any Java Exceptions were raised during the JKind 
        executions. 
        
        All assertions are performed as "subTest", meaning that an assertion
        failure will not end this method.
        
        '''

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
