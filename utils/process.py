'''
Created on Jun 28, 2013

@author: prmarti1
'''

import subprocess

def call( commandLineStr, verbose=False ):
    proc = subprocess.Popen( commandLineStr, stdout=subprocess.PIPE, shell=True )
    ( out, err ) = proc.communicate()
    if( verbose == True ):
        print( commandLineStr )
        if( ( out != None ) and ( len( out ) > 0 ) ):
            print( 'Output:' )
            print( out.decode() )
        if( ( err != None ) and ( len( out ) > 0 ) ):
            print( 'Errors:' )
            print( err.decode() )
    return( out, err )
