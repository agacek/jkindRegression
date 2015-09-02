
from jkind.jkind_exec import jkind_exec
from my_os.env_vars import checkEnvVars


if __name__ == '__main__':

    name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    solver = None

    checkEnvVars()
    propertyList = jkind_exec( name, solver )

    for each in propertyList:
        each.printAttrs()
