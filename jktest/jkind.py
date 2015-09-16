
import os
import subprocess
import xml.dom.minidom
from .results import JKindResult
from .results import ResultList


class JKind( object ):

    def __init__( self, fname, arg ):
        self._file = fname
        self._arg = arg
        # self._results = list()
        self._results = ResultList()


    def run( self ):

        # Execute JKind from the command line
        cmdLine = 'jkind ' + self._file + ' -xml ' + self._arg
        print( cmdLine )
        proc = subprocess.Popen( cmdLine, stdout = subprocess.PIPE, shell = True )
        ( out, err ) = proc.communicate()

        # Get the xml file that was generated and parse it for the attributes.
        # The xml parser will return an instance of the properties class
        xmlFile = self._file + '.xml'
        assert os.path.exists( xmlFile ) == True, 'XML File Exists?'
        self._parseXML( xmlFile )
        try:
            os.remove( xmlFile )
        except:
            pass

        self._results.sort()

        return self._results


    def _parseXML( self, xmlFile ):

        # Get the top level document
        doc = xml.dom.minidom.parse( xmlFile )

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


