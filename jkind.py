
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
    
    # Return the path to the xml file we expect to have created
    xmlFile = newSrc + '.xml'
    return xmlFile
