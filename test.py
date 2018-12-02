#!/usr/bin/env python3
from os import chdir, environ, getcwd, path
from subprocess import run
from history import history, handle_command, handle_special_case


'''
pwd             print working directory
cd              change directory
printenv        print all or part of environment
export          mark each name to be passed to child processes in the
                environment
unset           remove each variable or function name
exit            end process
history         many programs  read input from the user a line at a time. The
                GNU History library is able to keep track of those lines,
                associate arbitrary data with each line, and utilize
                information from previous lines in composing new ones.

'''


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


# change the path and set environ PWD as the path
def change_dir(dir_path):
    chdir(dir_path)
    environ['PWD'] = getcwd()


def cd(cd_args):
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
        elif _path is '~':
            if 'HOME' in environ:
                change_dir(environ['HOME'])
            else:
                change_dir(environ['XAUTHORITY'].strip('.Xauthority'))
        else:
            try:
                change_dir(path.abspath(_path))
            except FileNotFoundError:
                print('intek-sh: cd: ' + _path + ': No such file or directory')
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


def printenv(printenv_args):
    # if len type_in is 1 -> print all the environment
    if not check_args(printenv_args):
        for key in environ.keys():
            print(key + '=' + environ[key])
    else:  # print the value of the key(printenv_args[1])
        if printenv_args[1] in environ.keys():
            print(environ[printenv_args[1]])


def export(export_args):
    if check_args(export_args):
        variables = export_args[1:]
        for variable in variables:
            if '=' not in variable:
                environ[variable] = ''
            else:
                variable = variable.split('=')
                environ[variable[0]] = variable[1]


def unset(unset_args):
    if check_args(unset_args):
        variables = unset_args[1:]
        for variable in variables:
            if variable in environ.keys():
                del environ[variable]


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(type_in[1:]))
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(type_in[1:]))
    else:
        print('exit')


def run_file(file_args):
    cmd_not_found = False
    check = False
    if './' in file_args[0]:
        try:
            run(file_args[0])
        except PermissionError:
            print('intek-sh: ' + file_args[0] + ': Permission denied')
        except FileNotFoundError:
            print("intek-sh: " + file_args[0] + ": No such file or directory")
    else:
        try:
            # find all the possible paths
            PATH = environ['PATH'].split(':')
        except KeyError as e:
            print("intek-sh: " + file_args[0] + ": command not found")
            return e
        for item in PATH:
            if path.exists(item+'/'+file_args[0]):
                run([item+'/'+file_args.pop(0)]+file_args)
                check = True
                break
        if not check:  # if the command didn't run
            print("intek-sh: " + file_args[0] + ": command not found")
            cmd_not_found = True
    return cmd_not_found


def pwd(_):
    print(environ['PWD'])


def process_function(functions, command, arg):
    functions[command](arg)
    if 'exit' in command:
        return False
    else:
        return True


def handle_input(_args):
    _args = _args.split(' ')
    type_in = []
    for element in _args:
        if element:
            type_in.append(element)
    return type_in


def main():
    cmd_not_found = False
    special_cases = ['! ', '!', '!=']
    flag = True
    functions = {
            'pwd': pwd,
            'cd': cd,
            'printenv': printenv,
            'export': export,
            'unset': unset,
            'exit': sh_exit,
            'history': history,
            }
    history_lst = []
    while flag:
        _args = input('\033[92m\033[1mintek-sh$\033[0m ')
        # expand history_lst
        if not _args.startswith('!') and _args not in special_cases:
            history_lst.append(_args)
        # get args and check existence
        args, exist = handle_command(_args, history_lst)
        # when to continue or pass
        continue_flag, pass_flag, args = handle_special_case(exist, args)
        if continue_flag:
            continue
        elif pass_flag:
            pass

        type_in = handle_input(args)
        if type_in:
            if type_in[0] in functions.keys():
                if 'history' in type_in[0]:
                    flag = process_function(functions, type_in[0], history_lst)
                else:
                    flag = process_function(functions, type_in[0], type_in)
            else:
                cmd_not_found = run_file(type_in)
        if cmd_not_found and _args.startswith('!'):
            history_lst.append(_args)


if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
