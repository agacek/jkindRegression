
import os
import shutil


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
