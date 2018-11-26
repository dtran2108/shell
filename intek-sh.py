#!/usr/bin/env python3
import os
import subprocess
import glob


def enumerate(type_in):
    pass


def handle_globbing(type_in):
    glo = None
    index = None
    glob_ele = None
    glob_exist = False
    for i, e in enumerate(type_in):
        if '*' in e or '?' in e or '[' in e:
            index = i
            glo = glob.glob(e)
            glob_ele = e
            glob_exist = True
            break
    if index:
        type_in.pop(index)
    return type_in, glob_exist, glo


# =CD===========================================================================

def cd(type_in):

    # handle globbing
    type_in, glob_exist, glob_ele = handle_globbing(type_in)

    if glob_exist:
        i = 0
        while i < len(glob_ele):
            if os.path.isfile(glob_ele[i]):
                glob_ele.pop(i)
            i += 1
        glob_ele.sort()
        path = glob_ele[0]
    elif len(type_in) == 1:
        path = ''
    else:
        path = type_in[1]
    if path != '':
        try:
            os.chdir(os.path.abspath(path))
        except FileNotFoundError:
            print('intek-sh: cd: %s: No such file or directory' % path)
    elif path == '..':
        os.chdir('../')
    elif path == '':
        if 'HOME' in os.environ:
            os.chdir(os.environ['HOME'])
        else:
            print('intek-sh: cd: HOME not set')


# =PRINTENV=====================================================================

def printenv(type_in):
    if len(type_in) == 1:
        for key in os.environ.keys():
            print(key + '=' + os.environ[key])
    else:
        variable = type_in[1]
        if variable in os.environ.keys():
            print(os.environ[variable])
        else:
            return


# =EXPORT=======================================================================

def export(type_in):
    if len(type_in) == 1:
        return
    variables = type_in[1:]
    for variable in variables:
        if '=' not in variable:
            os.environ[variable] = ''
        else:
            variable = variable.split('=')
            os.environ[variable[0]] = variable[1]


# =UNSET========================================================================

def unset(type_in):
    if len(type_in) == 1:
        return
    variables = type_in[1:]
    for variable in variables:
        if variable in os.environ.keys():
            del os.environ[variable]
        else:
            return


# =EXIT=========================================================================

def sh_exit(type_in):
    if len(type_in) == 1:
        print('exit')
    elif type_in[1].isdigit():
        print('exit')
    else:
        print('exit\nintek-sh: exit:')


# =RUN_FILE=====================================================================

def run_file(type_in):
    flag = False

    # handle globbing
    glo = None
    index = None
    glob_ele = None
    glob_exist = False
    for i, e in enumerate(type_in):
        if '*' in e or '?' in e or '[' in e:
            index = i
            glo = glob.glob(e)
            glob_ele = e
            glob_exist = True
            break
    if index:
        type_in.pop(index)

    # run file in current directory
    if './' in type_in[0]:
        try:
            subprocess.run(type_in[0])
        except PermissionError:
            print('intek-sh: ' + type_in[0] + ': Permission denied')
        except FileNotFoundError:
            print("intek-sh: " + type_in[0] + ": No such file or directory")
    else: # run file in PATH
        try:
            PATH = os.environ['PATH'].split(':')
        except KeyError:
            print("intek-sh: " + type_in[0] + ": command not found")
            return
        for item in PATH:
            if os.path.exists(item+'/'+type_in[0]):

                # if there is globbing
                if glob_exist:
                    if glo != []:
                        subprocess.run([item+'/'+type_in.pop(0)]+type_in+glo)
                    else: # if there's no file match globbing
                        print('intek-sh: %s: cannot access \'%s\': No such'
                              ' file or directory' % (type_in[0], glob_ele))

                else:
                    subprocess.run([item+'/'+type_in.pop(0)]+type_in)

                flag = True
                break
        if not flag:
            print("intek-sh: " + type_in[0] + ": command not found")


# =MAIN=========================================================================

def get_input():
    type_in = input('intek-sh$ ')
    while type_in == '' or type_in == ' ':
        type_in = input('intek-sh$ ')
    # handle multiple spaces
    type_in = type_in.split(' ')
    while '' in type_in:
        type_in.remove('')
    return type_in[0], type_in


def main():
    flag = True
    while flag:
        try:
            command, type_in = get_input()
        except EOFError:
            return
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'cd':
            cd(type_in)
        elif command == 'printenv':
            printenv(type_in)
        elif command == 'export':
            export(type_in)
        elif command == 'unset':
            unset(type_in)
        elif command == 'exit':
            sh_exit(type_in)
            flag = False
        else:
            run_file(type_in)


if __name__ == '__main__':
        main()
