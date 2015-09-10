
import os
from test_runner.internaldata import InternalData
from test_runner.runner import runtest

# Need to set the current working directory
os.chdir( 'c:/users/prmarti1/smaccm/jkind_test/test_workspace/jkindregression' )

file = './unit_test/test_files/tuple.lus'
print( os.path.abspath( file ) )

assert os.path.exists( os.path.abspath( file ) ) == True, 'Assert File Exists'

InternalData().setTestPath( file )

runtest()
