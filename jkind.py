
from utils.process import call
from utils.dirs import copyFile 
import os


def jkind( filename, solver ):
    '''
    '''
    print( os.getcwd() )
    
    # Copy the file to the cwd
    dst = os.path.join( os.getcwd(), 'output' )    
    newSrc = copyFile( filename, dst )
    
    a = 'jkind ' + newSrc + ' -xml'
    call( a )
