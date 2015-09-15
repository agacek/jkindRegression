
import os
import shutil
import fnmatch


def copyFile( filename, dstDir ):
    '''
    Copy a file to a new directory
    
    Attempts to make the new directory, if exists will catch the
    exception. Attempts to copy the specified file to the new directory
    
    Returns the new path+filename of the copied file.
    '''
    try:
        os.mkdir( dstDir )
    except FileExistsError:
        pass

    shutil.copy( filename, dstDir )

    rv = os.path.join( dstDir, os.path.basename( filename ) )

    return rv


def deleteFile( filename ):
    try:
        os.remove( filename )
    except:
        pass


def parseFiles( arg, recurse = True ):

    # Format the path argument slashes
    arg = os.path.abspath( arg )

    # Just see if this even exists
    assert os.path.exists( arg )

    # If this is a file, then just return it as a list
    if( os.path.isfile( arg ) == True ):
        return [arg]

    # Otherwise this is a directory, search for the *.lus files and
    # build a list of the files.
    l = list()
    for filename in _walk( arg, recurse, '*.lus' ):
        l.append( filename )
    return l


def _walk( root = '.', recurse = True, pattern = '*' ):
    '''
    Private Function:
    
    Arguments:
    root - the top folder path to walk through
    recurse - if True will go through sub-folders
    patter - file extension to look for (i.e. *.c)
    
    Description:
    Generator for walking a directory tree.
    Starts at specified root folder, returning files
    that match our pattern. Optionally will also
    recurse through sub-folders.
    '''
    for path, subdirs, files in os.walk( root ):
        for name in files:
            if fnmatch.fnmatch( name, pattern ):
                yield os.path.join( path, name )
        if not recurse:
            break
