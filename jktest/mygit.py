import os
import subprocess



def clone( http, lclDir, branch = None, pullIfExists = False ):

    # Look for the ../*.git file. If it exists, then decide whether to Pull
    # from the remote or not. If we're not going to pull return False to
    # indicate we didn't do anything.

    gitFile = http.split( '/' )
    gitFile = gitFile[len( gitFile ) - 1]

    testGit = os.path.join( lclDir, '.git' )
    exists = os.path.exists( testGit )

    if( exists == True and pullIfExists == False ):
        print( 'Exists, no Pull' )
        return True

    if( exists == True and pullIfExists == True ):
        # Do a git pull
        print( 'Exists, Pull' )
        saveDir = os.getcwd()
        os.chdir( lclDir )
        _call( 'git pull' )
        os.chdir( saveDir )
        return True

    # Otherwise we need to clone
    if( isinstance( branch, str ) == True ):
        bcmd = '-b ' + branch
    else:
        bcmd = ''
    cmd = 'git clone {} {} {}'.format( http, lclDir, bcmd )
    print( 'Clone ' + cmd )
    _call( cmd )

    # Check if it worked
    if( os.path.exists( testGit ) == True ):
        return True

    # Uh-oh
    return False


def _call( cmdLine ):
    proc = subprocess.Popen( cmdLine, stdout = subprocess.PIPE, shell = True )
    ( out, err ) = proc.communicate()
