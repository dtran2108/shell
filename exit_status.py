def replace_the_pattern(pattern, arg, exit_code):
    new_arg = arg.replace(pattern, exit_code)
    replace_things.append(new_arg)


def get_exit_status(arg, exit_code):
    global replace_things
    replace_things = []
    if '$?' in arg:
        replace_the_pattern('$?', arg, exit_code)
    elif '${?}' in arg:
        replace_the_pattern('${?}', arg, exit_code)
    return replace_things
