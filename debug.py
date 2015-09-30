'''
This module can be used as a debug entry point when using the PyDev Eclipse
plug-in.

Only retained as a convenience and not intended for general use
or maintenance.

'''

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
# file = 'c:/temp'
file = 'c:/temp/turing.lus'
print( os.path.abspath( file ) )

SetupConfig().setTestFiles( file, False )

runsuite()
