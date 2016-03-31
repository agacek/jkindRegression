'''
This module contains the class that is the data store for required information
to run the JKind Regression Test Suite.
 
'''

import os
import copy
import fnmatch
import xml.dom.minidom
from itertools import product
# from docutils.parsers.rst.directives import path


class SetupConfig( object ):
    '''
    **Public Class**
    
    This class processes arguments and inputs required to run the JKind
    Regression Test Suite. It also acts as the data store from which modules
    may retrieve the processed and stored data. 
    
    Typically the "set" methods accept inputs from the command line
    arguments or the GUI. However if alternate applications are derived there
    are no restrictions on how or when to access this class.
    
    This class implements the **Borg** Design Pattern. This DP is similar to a 
    Singleton, except that it is explicitly instantiated and contains shared
    data. Each instantiation is a unique object but all objects share the internal
    __dict__ and thus all share the data.
    
    '''

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _files = None
    _args = None
    _logfile = None
    _jkindfile = None
    _java = None
    _quiet = False


    def __init__( self ):
        '''
        **Constructor**
        
        Sets the shared state per the Borg Design Pattern.
        
        '''

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one

        # Set the strings to be the beginning and end tags. These are used to
        # write out for the test cases.
        self._beginTestTag = 'BEGIN TEST OF: '
        self._endTestTag = 'END TEST OF '


    def setTestArguments( self, argumentsXmlFile ):
        '''
        **Public Method**
        
        Reads the Arguments XML file and collects all of the
        Argument Group elements. Creates all the possible combinations
        of argument strings between the items in each of the 
        Argument Groups. 
        
        :param argumentsXmlFile: path and filename of the XML Argument File
        :type argumentsXmlFile: str
        :return: n/a:
        :asserts: argumentsXmlFile file exists
        
        '''        
        if( os.path.exists( argumentsXmlFile ) != True ): 
            print( '*** ERROR: Arguments file does not exist -> ' + argumentsXmlFile )
        assert os.path.exists( argumentsXmlFile )
        
        argsListList = list()
        doc = xml.dom.minidom.parse( argumentsXmlFile )
        groups = doc.getElementsByTagName( 'ArgumentGroup' )

        for eachGroup in groups:
            args = eachGroup.getElementsByTagName( 'arg' )
            l = list()

            for eachArg in args:
                try:
                    l.append( eachArg.firstChild.data )
                except AttributeError:
                    l.append( '' )

            argsListList.append( l )

        self._args = list()
        for args in product( *argsListList ):
            # Convert the args tuple to a single string
            argStr = ''
            for each in args:
                argStr += each
                argStr += ' '
            self._args.append( argStr )


    def getTestArguments( self ):
        '''
        **Public Method**
        
        Returns a deep-copy of the list of all the possible argument 
        combinations.
        
        :return: List of argument strings if initialized, otherwise None
        :rtype: list[str...] *or* None
                
        '''
        if( isinstance( self._args, list ) == True ):
            return copy.deepcopy( self._args )
        else:
            return None


    def setTestFiles( self, fileOrPath, recurse ):
        '''
        **Public Method**
        
        Stores the filenames to test. Accepts either a single filename, a list of
        filenames or a folder to search for Lustre files.
        
        :param fileOrPath: filename(s) or path
        :type fileOrPath: str *or* list of str's
        
        :param recurse: If folder specified, flag to recursively 
                        search sub-folders
        :type recurse: bool
        
        :return: n/a:
        
        :asserts: - If list is supplied, list length > 0
                  - File(s) or folder path exists
        
        '''

        # Test to see if this is list-type. If so assume that it's a list of filenames.
        # We DO NOT support a list of directories.
        if( isinstance( fileOrPath, list ) == True ):
            self._files = list( fileOrPath )

            if( len( fileOrPath) < 1 ):
                print( '*** ERROR: No file or path selected')
            assert len( fileOrPath ) > 0  # Make sure this isn't an empty list

            # Test that the files exist
            for each in self._files:
                if( os.path.exists( each ) != True ):
                    print( '*** ERROR: Selected file/path does not exist -> ' + each )
                assert os.path.exists( each ), 'User specified file/path does not exist'

        # Otherwise we believe we've received either a single file name or a
        # directory for us to search for *.lus files.
        else:
            # Make sure this even exists
            if( os.path.exists( fileOrPath ) != True ):
                print( '*** ERROR: User specified file/path does not exist-> ' + fileOrPath )
            assert os.path.exists( fileOrPath ), 'User specified file/path does not exist'

            # Format the path argument slashes
            fileOrPath = os.path.abspath( fileOrPath )

            # If this is a file, then just return it as a list
            if( os.path.isfile( fileOrPath ) == True ):
                self._files = [fileOrPath]

            else:
                # Otherwise this is a directory, search for the *.lus files and
                # build a list of the files.
                l = list()
                for filename in self._walk( fileOrPath, recurse, '*.lus' ):
                    l.append( filename )

                self._files = l


    def getTestFiles( self ):
        '''
        **Public Method**
        
        Returns a deep-copy of the list of all the files to test.
        
        :return: List of files if initialized, otherwise None
        :rtype: list[str...] *or* None
                
        '''
        if( isinstance( self._files, list ) == True ):
            return copy.deepcopy( self._files )
        else:
            return None


    def setLogFile( self, fname ):
        '''
        **Public Method**
        
        Sets the log file. No error checking on type of if the path exists.
        
        :param fname: path and filename of the log file
        :type fname: str
        
        :return: n/a:
        
        '''
        self._logfile = fname


    def getLogFile( self ):
        '''
        **Public Method**
        
        Returns the log file path and filename. Initialized to None.
        
        :return: Filename if set, otherwise None
        :rtype: str *or* None
        
        '''
        return self._logfile


    def setJkindFile( self, path ):
        '''
        **Public Method**
        
        Set the fully qualified path of the desired alternate JKind jar file.
        If not explicitly set the application will use the default JKind that
        is on the system path.
        
        :param path: Fully qualified path to alternate JKind jar file
        :type path: str
        
        :return: n/a:
        
        '''
        self._jkindfile = path


    def getJkindFile( self ):
        '''
        **Public Method**
        
        Getter method to retrieve the path to the specified alternate JKind
        jar file to run. If an alternate jar was not specified via the
        complementary set method, will return None.
        
        :return: Fully qualified path if set, None otherwise.
        :rtype: str *or* None
        
        '''
        return self._jkindfile


    def setJava( self, java ):
        '''
        **Public Method**
        
        Set an alternate Java executable to run. If not explicitly set the
        application will run whatever Java is on the system path.
        
        :param java: Fully qualified path to alternate Java executable
        :type java: str
        
        :return: n/a:
        
        '''
        self._java = java


    def getJava( self ):
        '''
        **Public Method**
        
        Getter method to retrieve the path to the alternate Java executable,
        if specified
        
        :return: Fully qualified path if set, None otherwise.
        :rtype: str *or* None
        
        '''
        return self._java


    def setQuiet( self, TorF ):
        '''
        **Public Method**
        
        Sets the quiet flag, which indicates that all "errors" reported by
        jkind that are not failures are suppressed in the output. These are
        raised when non-supported argument combinations have been selected or
        if all proving engines are turned off based upon the argument combos.
        
        :param TorF: Set quiet flag on or off
        :type TorF: boolean
        
        :return: n/a:
        
        '''
        self._quiet = TorF


    def isQuiet( self ):
        '''
        **Public Method**
        
        Returns the quiet flag, to indicate whether non-failing errors should
        be suppressed in the output logs.
        
        :return: the quiet flag
        :rtype: boolean
        
        '''
        return self._quiet


    def getBeginTestTag( self ):
        '''
        **Public Method**
        
        Getter method for the beginning test tag string. 
        
        :return: begin test tag
        :rtype: str
        
        '''
        return self._beginTestTag


    def getEndTestTag( self ):
        '''
        **Public Method**
        
        Getter method for the end test tag string.
        
        :return: end test tag
        :rtype: str
        
        '''
        return self._endTestTag


    def _walk( self, root = '.', recurse = True, pattern = '*' ):
        '''
        **Private Method**
                                
        Generator for walking a directory tree.
        Starts at specified root folder, returning files
        that match our pattern. Optionally will also
        recurse through sub-folders.
                
        :param root: the top folder path to walk through
        :type root: str
        :param recurse: if True will go through sub-folders
        :type recurse: bool
        :param pattern: file extension to look for (i.e. \*.c, \*.py)
        :type pattern: str
        
        :yield: path+filename
        :ytype: str
               
        '''
        for path, subdirs, files in os.walk( root ):
            for name in files:
                if fnmatch.fnmatch( name, pattern ):
                    yield os.path.join( path, name )
            if not recurse:
                break
