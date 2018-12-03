#!/usr/bin/env python3

'''
Event Designators
       An event designator is a reference to a command line entry in
       the history list.  Unless the reference is absolute, events are rela‐
       tive to the current position in the history list.

       !      Start a history substitution, except when followed by a blank,
              newline, = or (.
       !n     Refer to command line n.
       !-n    Refer to the current command minus n.
       !!     Refer to the previous command.  This is a synonym for `!-1'.
       !string
              Refer to the most recent command preceding the current position
              in the history list starting with string.
       !?string[?]
              Refer  to  the most recent command preceding the current position
              in the history list containing string.  The trailing ? may
              be omitted if string is followed immediately by a newline.
       ^string1^string2^
              Quick substitution.  Repeat the last command, replacing string1
              with string2.  Equivalent to ``!!:s/string1/string2/''
       !#     The entire command line typed so far.

'''


def history(history_lst):
    for index, element in enumerate(history_lst):
        # justify columns
        _order = str(index+1).rjust(len(str(len(history_lst))), ' ')
        command = element.ljust(len(max(history_lst, key=len)), ' ')
        print('  ' + _order + '  ' + command)


# handle special case of '!'
def handle_special_case(exist, args):
    continue_flag = False
    pass_flag = False
    if args.startswith('!'):
        # no matched event in history_lst
        if not exist:
            print('intek-sh: ' + args + ': event not found')
            continue_flag = True
        else:
            # command starts with ! and followed by a blank space
            if len(args) is 1 or args == '! ':
                continue_flag = True
            # command starts with '!=' -> command not found
            elif args[1] is '=':
                pass_flag = True
            # command is only '!#'
            elif args[1] is '#':
                print(' ')
                continue_flag = True
            # command type: '! randomstring'
            elif len(args) > 2:
                args = args[2:]
                pass_flag = True
    # elif bad_specifier:
    #     continue_flag = True
    return continue_flag, pass_flag, args


# replace args as cmd and print it
def print_args(args, cmd):
    args = cmd
    # if not bad_specifier:
    print(args)
    return args, True


def handle_exclamation_n_hashtag(arg, index, args_lst):
    global bad_specifier
    bad_specifier = False
    if arg == '!#':
        alternative = args_lst[:index]
        args_lst.pop(index)
        for i, element in enumerate(alternative):
            args_lst.insert(index + i, element)
    elif arg[:3] == '!#:' and arg[3:].isdigit():
        pos = int(arg[3:])
        alternative = args_lst[:index]
        args_lst.pop(index)
        try:
            args_lst.insert(index, alternative[pos])
        except IndexError:
            print('intek-sh: ' + arg[2:] + ': bad word specifier')
            bad_specifier = True
    return args_lst


def handle_command(args, history_lst):
    exist = False
    hashtag = False
    if args.startswith('!'):
        if len(args) is 1 or args[1] is ' ' or args[1] is '=':
            return args, True, hashtag, continue_flag
        elif args[1] is '(':
            return args[0], exist, hashtag, continue_flag
        elif args[1] is '#':
            return args, True, hashtag, continue_flag

        # command type: '!?'
        elif args[1:].startswith('?'):
            args = args.strip('!?')
            for cmd in reversed(history_lst):
                if args in cmd:
                    args, exist = print_args(args, cmd)
                    break

        # command type: '!!'
        elif args[1:].startswith('!'):
            new_args = args.replace('!!', history_lst[len(history_lst) - 1])
            args, exist = print_args(args, new_args)

        # command type: '!n'
        elif args[1].isdigit():
            prefix = ''
            for word in args[1:]:
                if word.isdigit():
                    prefix += word
                else:
                    break
            number = int(prefix)
            if (number-1) < len(history_lst):
                new_args = args.replace('!' + prefix, history_lst[number-1])
                args, exist = print_args(args, new_args)

        # command type: '!-n'
        elif args[1] is '-' and args[2].isdigit():
            prefix = ''
            for word in args[2:]:
                if word.isdigit():
                    prefix += word
                else:
                    break
            number = int(prefix)
            if number < len(history_lst):
                new_args = args.replace('!' + '-' + prefix,
                                        history_lst[len(history_lst) - number])
                args, exist = print_args(args, new_args)

        # command type: '!string'
        elif args[1].isalpha():
            if ' ' in args:
                args_lst = args.split(' ')
                for cmd in reversed(history_lst):
                    if cmd.startswith(args[0]):
                        args_lst.pop(0)
                        args_lst.insert(0, cmd)
                        args, exist = print_args(args, ' '.join(args_lst))
                        break
            else:
                print(2)
                for cmd in reversed(history_lst):
                    if cmd.startswith(args):
                        args, exist = print_args(args, cmd)
                        break
    else:  # command type: '!#'
        if '!#' in args:
            hashtag = True
            args_lst = args.split(' ')
            for index, arg in enumerate(args_lst):
                if '!#' in arg:
                    args_lst = handle_exclamation_n_hashtag(arg, index,
                                                            args_lst)
            args, exist = print_args(args, ' '.join(args_lst))
    return args, exist, hashtag
