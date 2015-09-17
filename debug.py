
import os
import platform
from jktest.config import SetupConfig
from jktest.testsuite import runsuite

# Need to set the current working directory
if( platform.system() == 'Darwin' ):
    wdir = '/Users/paul/code/jkind_test/test_workspace/jkindRegression'
else:
    wdir = 'c:/users/prmarti1/smaccm/jkind_test/test_workspace/jkindregression'
os.chdir( wdir )
assert os.path.exists( wdir )


SetupConfig().setTestArguments( 'test_arguments.xml' )


# file = './unit_test/test_files/tuple.lus'
file = 'c:/temp'
print( os.path.abspath( file ) )
# assert os.path.exists( os.path.abspath( file ) ) == True, 'Assert File Exists'

SetupConfig().setTestFiles( file, False )

runsuite()
