from os import environ
from input_excuting import check_args


def export(export_args):
    exit_code = None
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
                exit_code = 0
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]
                exit_code = 0
    return exit_code
