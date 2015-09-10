import os

DEFAULT_XML_FILE = 'test_config.xml'


class InternalData( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _xml_config_file = DEFAULT_XML_FILE
    _output_dir = os.path.join( os.getcwd(), 'output' )
    _verbose = False
    _path = None
    _recurse = False

    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one

    def getTestPath( self ):
        return self._path

    def setTestPath( self, path ):
        self._path = path

    def getRecurseFlag( self ):
        return self._recurse

    def setRecurseFlag( self, recur ):
        self._recurse = recur

    def getXmlConfigFile( self ):
        return self._xml_config_file

    def setXmlConfigFile( self, newXmlFile ):
        self._xml_config_file = newXmlFile

    def getOutputDir( self ):
        return self._output_dir

    def setOutputDir( self, newDir ):
        self._output_dir = newDir

    def setVerbose( self, TorF ):
        self._verbose = TorF

    def isVerbose( self ):
        return self._verbose

