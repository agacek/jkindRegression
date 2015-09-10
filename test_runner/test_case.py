import os
import xml.dom.minidom
from itertools import product
from my_os.process import call
from my_os.dirs import deleteFile
from .testdata import RunResult
from .testdata import XmlProperties
from .internaldata import InternalData
from .logger import Logger


class TestCase( object ):

    def __init__( self, fileUnderTest ):
        self._fileUnderTest = fileUnderTest
        assert os.path.exists( self._fileUnderTest ) == True, 'File Under Test Exists?'

        self._testPass = False
        self._fileResults = list()
        Logger().logFile( self._fileUnderTest )


    def runTest( self ):

        # Read the desired arguments from the XML configuration file.
        # The returned value is a list-of-lists.
        argumentsLists = self._getArguments()

        # Run JKind, iterating through the combinations of arguments.
        for args in product( *argumentsLists ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '

            # Run JKind for the given set of arguments
            self._jkindRun( argStr )

        # Validate the results
        return self._validate()


    def _jkindRun( self, arguments ):

        Logger().logArguments( arguments )
        cmdLine = 'jkind ' + self._fileUnderTest + ' -xml ' + arguments
        opt, err = call( cmdLine )

        # Get the xml file that was generated and parse it for the attributes.
        # The xml parser will return an instance of the properties class
        xmlFile = self._fileUnderTest + '.xml'
        assert os.path.exists( xmlFile ) == True, 'XML File Exists?'
        xmlProps = self._parseXML( xmlFile )

        # Instantiate the File Results and add the properties we just got.
        results = RunResult( self._fileUnderTest, arguments, xmlProps )

        # Add the results to our internal list for later validation
        self._fileResults.append( results )

        # Delete the xml file so we don't get fooled if a subsequent jkind
        # run fails.
        deleteFile( xmlFile )


    def _validate( self ):
        # Check that all the results are the same
        tmpList = self._fileResults.copy()
        key = tmpList.pop()

        if( InternalData().isVerbose() == True ):
            Logger().logString( '\nVALIDATE' )

        for each in tmpList:
            if( key.equal( each ) == False ):
                self._testPass = False
                break
            else:
                self._testPass = True

            if( InternalData().isVerbose() == True ):
                s = key.argumentStr() + ' <- COMPARE TO -> ' + each.argumentStr()
                s += '  : ' + str( self._testPass )
                Logger().logString( s )

        # Logger().logResult( self._testPass )

        return self._testPass


    def _parseXML( self, filename ):

        # Get the top level document
        doc = xml.dom.minidom.parse( filename )

        # Get a list of all the XmlProperties elements
        properties = doc.getElementsByTagName( 'Property' )

        # Initialize a list to contain the XmlProperties instantiations
        propList = list()

        for each in properties:

            # Instantiate our data
            theProp = XmlProperties()

            # Get the Name of the XmlProperties
            theProp.name = each.getAttribute( 'name' )

            # Get the Answer attribute. From that get the validity and the source
            # Assumes that there is only one Answer, etc...
            answerAttr = each.getElementsByTagName( 'Answer' )[0]
            theProp.answer = answerAttr.firstChild.data
            theProp.source = answerAttr.getAttribute( 'source' )

            # Get the K attribute and fill in the value
            kAttr = each.getElementsByTagName( 'K' )[0]
            theProp.K = kAttr.firstChild.data

            # Add to our list of Properties
            propList.append( theProp )

        return propList


    def _getArguments( self ):

        argsList = list()
        doc = xml.dom.minidom.parse( InternalData().getXmlConfigFile() )
        groups = doc.getElementsByTagName( 'ArgumentGroup' )

        for eachGroup in groups:
            args = eachGroup.getElementsByTagName( 'arg' )
            l = list()

            for eachArg in args:
                try:
                    l.append( eachArg.firstChild.data )
                except AttributeError:
                    l.append( '' )

            argsList.append( l )

        return argsList
