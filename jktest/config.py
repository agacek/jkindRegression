'''
This module contains the class that is the data store for required information
to run the JKind Regression Test Suite.
 
'''

import os
import copy
import fnmatch
import xml.dom.minidom
from itertools import product


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


    def __init__( self ):
        '''
        **Constructor**
        
        Sets the shared state per the Borg Design Pattern.
        
        '''

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


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

            assert len( fileOrPath ) > 0  # Make sure this isn't an empty list

            # Test that the files exist
            for each in self._files:
                assert os.path.exists( each ), 'User specified file/path does not exist'

        # Otherwise we believe we've received either a single file name or a
        # directory for us to search for *.lus files.
        else:
            # Make sure this even exists
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
