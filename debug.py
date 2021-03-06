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
from gui.launch import launchGUI

# Need to set the current working directory
if( platform.system() == 'Darwin' ):
    wdir = '/Users/paul/code/jkind_test/test_workspace/jkindRegression'
else:
    wdir = 'c:/users/prmarti1/smaccm/jkind_ci/jkindregression'
os.chdir( wdir )
assert os.path.exists( wdir )

SetupConfig().setTestArguments( 'default_args.xml' )

# file = './unit_test/test_files/tuple.lus'
# file = 'c:/temp'
#file = 'c:/temp/records.lus'
file = r'C:\Users\prmarti1\smaccm\jkind_ci\jkind\testing'
print( os.path.abspath( file ) )

SetupConfig().setTestFiles( file, False )

#runsuite()
launchGUI()
