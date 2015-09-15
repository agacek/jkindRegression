
import os
import platform
from test_runner.internaldata import ConfigData
from test_runner.runner import runtest

# Need to set the current working directory
if( platform.system() == 'Darwin' ):
    wdir = '/Users/paul/code/jkind_test/test_workspace/jkindRegression'
else:
    wdir = 'c:/users/prmarti1/smaccm/jkind_test/test_workspace/jkindregression'
os.chdir( wdir )
assert os.path.exists( wdir )

file = './unit_test/test_files/tuple.lus'
print( os.path.abspath( file ) )
assert os.path.exists( os.path.abspath( file ) ) == True, 'Assert File Exists'

ConfigData().setTestPath( file )

runtest()
