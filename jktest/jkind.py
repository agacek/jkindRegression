'''
This module contains the JKind class for execution and 
collection of the results.

'''

import os
import subprocess
import xml.dom.minidom
from .results import JKindResult
from .results import ResultList


class JKind( object ):
    '''
    **Public Class**
    
    This class performs the command line call to execute JKind on the desired
    file and argument set and collects the results.

    '''

    def __init__( self, fname, arg ):
        '''
        **Constructor**
        
        :param fname: lustre filename to run
        :type fname: str
        :param arg: arguments to execute
        :type arg: str

        '''
        self._file = fname
        self._arg = arg
        self._results = ResultList()


    def run( self ):
        '''
        **Public Method**
        
        Constructs the command line string to run JKind on the file with the
        argument set. Calls _parseXML to read and collect the results.
        
        :return: If JKind executed properly, a ResultList of JKindResult 
                 objects containing each Property generated in the JKind
                 execution. Otherwise None.

        :rtype: ResultList[JKindResult...] *or* None

        '''

        # Execute JKind from the command line
        cmdLine = 'jkind ' + self._file + ' -xml ' + self._arg
        print( cmdLine )
        proc = subprocess.Popen( cmdLine, stdout = subprocess.PIPE, shell = True )
        ( out, err ) = proc.communicate()

        # Check that jkind ran. Some flags aren't compatible with some solvers.
        if( out.decode().lower().startswith( 'error' ) == True ):
            self._results = None
            print( '    >> Skipped: Incompatible argument combination' )

        # Happy path...
        else:
            # Parse the XML file that was generated for this test. The results
            # are stored in class member data
            self._parseXML()

        # Give back our results
        return self._results


    def _parseXML( self ):
        '''
        **Private Method**

        Constructs the XML results filename from the lustre filename. Opens the
        XML file and reads each of the "Property" elements. Instantiates a
        JKindResult object and stores the "name", "Answer", and "K" value for
        each Property. Appends each JKindResult object to the ResultList 
        member.

        :return: n/a:

        '''

        # The XML file should be the same name as our *.lus file, just with
        # the xml extension.
        xmlFile = self._file + '.xml'
        assert os.path.exists( xmlFile ) == True, 'XML File Exists?'

        # Get the top level document
        doc = xml.dom.minidom.parse( xmlFile )

        # print( 'READ XML: ' + xmlFile )

        # Get a list of all the XmlProperties elements
        properties = doc.getElementsByTagName( 'Property' )

        for each in properties:

            # Instantiate our data
            res = JKindResult( self._file, self._arg )

            # Get the Name of the XmlProperties
            res['name'] = each.getAttribute( 'name' )


            # Get the Answer attribute. From that get the validity and the source
            # Assumes that there is only one Answer, etc...
            answerAttr = each.getElementsByTagName( 'Answer' )[0]
            res['answer'] = answerAttr.firstChild.data
            # res['source'] = answerAttr.getAttribute( 'source' )

            # Get the K attribute and fill in the value if available
            try:
                kAttr = each.getElementsByTagName( 'K' )[0]
                res['K'] = kAttr.firstChild.data
            except:
                res['K'] = ''

            # Add to our list of Properties
            self._results.append( res )

        # Delete the XML file we generated for this run so we don't get fooled
        # later by a stale file when a jkind run failed.
        try:
            os.remove( xmlFile )
        except:
            pass

        # Sort the list to make equality testing easier later on
        self._results.sort()
