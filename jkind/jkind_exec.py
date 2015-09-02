
import os
from my_os.process import call
from my_os.dirs import copyFile
from ._myxml import parseXML


def jkind_exec( filename, solver ):
    '''
    '''
    print( os.getcwd() )

    # Copy the file to the cwd
    dst = os.path.join( os.getcwd(), 'output' )
    newSrc = copyFile( filename, dst )

    a = 'jkind ' + newSrc + ' -xml'
    call( a )

    # Get the xml file that was generated and parse it for the attributes.
    # The xml parser will return a list of the properties.
    xmlFile = newSrc + '.xml'
    return parseXML( xmlFile )
