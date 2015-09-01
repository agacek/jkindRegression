
from jkind import jkind
from utils.env_vars import checkEnvVars

if __name__ == '__main__':
    
    name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    solver = None
    
    checkEnvVars()       
    jkind( name, solver )
    
