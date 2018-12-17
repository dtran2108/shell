from sys import exit
from input_excuting import check_args


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(exit_args[1:]))
            exit_code = int(' '.join(exit_args[1:]))
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(exit_args[1:]))
            exit_code = 0
    else:
        print('exit')
        exit_code = 0
    exit(exit_code)
