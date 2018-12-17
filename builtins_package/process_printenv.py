from os import environ
from input_excuting import check_args


def printenv(printenv_args):
    # if len type_in is 1 -> print all the environment
    exit_code = None
    if not check_args(printenv_args):
        exit_code = 0
        for key in environ.keys():
            print(key + '=' + environ[key])
    else:  # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            exit_code = 0
            print(environ[printenv_args[1]])
        else:
            exit_code = 1
    return exit_code
