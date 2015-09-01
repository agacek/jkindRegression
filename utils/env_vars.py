
import os


def checkEnvVars():
    
    jkindFound = False
    yicesFound = False
    
    l = list( os.environ.values() )
    for each in l:
        a = each.lower()
        if( a.find( 'jkind' ) >= 0 ):
            jkindFound = True
        if( a.find( 'yices' ) >= 0 ):
            yicesFound = True
            
    assert jkindFound == True, 'jkind environment variable not found'
    assert yicesFound == True, 'yices environment variable not found'         
