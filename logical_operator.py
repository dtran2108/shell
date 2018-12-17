from input_excuting import input_excuting
from os import environ

#  returns a list seperated by the operator && or ||
def split_operator(args, operator):
    args = args.split(sep=operator)
    return args


def handle_and(args, functions):
    #  if the first command succeeds, excute the second
    curpath = environ['PWD']
    exit_code = 0
    flag = False
    for item in args:
        if exit_code == 0:
            flag, exit_code = input_excuting(item, functions, curpath,
                                             exit_code)
    return flag, exit_code


def handle_or(args, functions):
    #  if the first command fails, excute the second
    curpath = environ['PWD']
    exit_code = 1
    flag = False
    for item in args:
        while exit_code != 0:
            flag, exit_code = input_excuting(item, functions, curpath,
                                             exit_code)
            break
    return flag, exit_code


def handle_logical_operator(args, functions):
    _args = args
    if "&&" in _args:
        _args = split_operator(_args, "&&")
        flag, exit_code = handle_and(_args, functions)
    if "||" in _args:
        _args = split_operator(_args, "||")
        flag, exit_code = handle_or(_args, functions)
    return flag, exit_code
