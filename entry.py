
from test_runner.runner import go
from my_os.env_vars import checkEnvVars


if __name__ == '__main__':

    name = r'C:\Users\prmarti1\smaccm\jkind_test\jkind\testing\pre.lus'
    checkEnvVars()

    go( name )
