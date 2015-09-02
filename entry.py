
from jkind import jkind
from utils.env_vars import checkEnvVars
from myxml import parseXML

if __name__ == '__main__':
    
    name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    solver = None
    
    checkEnvVars()       
    xmlFile = jkind( name, solver )
    
    parseXML( xmlFile )
