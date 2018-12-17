from os import environ
from input_excuting import check_args


def unset(unset_args):
    exit_code = None
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]
                exit_code = 0
    return exit_code
