
import os


def checkEnvVars():

    jkindFound = False
    yicesFound = False
    cvcFound = False

    l = list( os.environ.values() )
    for each in l:
        a = each.lower()
        if( a.find( 'jkind' ) >= 0 ):
            jkindFound = True
        if( a.find( 'yices' ) >= 0 ):
            yicesFound = True
        if( a.find( 'cvc' ) >= 0 ):
            cvcFound = True

    assert jkindFound == True, 'jkind environment variable not found'
    assert yicesFound == True, 'yices environment variable not found'
    assert cvcFound == True, 'cvc environment variable not found'
