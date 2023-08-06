def arg2str(argument):
    argument = list(argument.keys())[0]
    if argument[0] == "-":
        return f"[{argument}]"
    else:
        if '?' in argument:
            argument = argument.split('=')[0]
            return f"[{argument}]"
        return f"<{argument}>"


def print_args(cmd, print_args: bool):
    for arg in cmd.args:
        arg_name, arg_descr = list(arg.items())[0]
        is_switch = arg_name[0] == "-"
        # skip args when print_args is false and item is not a switch
        if not print_args and not is_switch:
            continue
        # break loop when print args is tue and switches where reached
        if print_args and is_switch:
            return
        arg_default = None
        if '=' in arg_name:
            arg_name, arg_default = arg_name.split('=', 1)
        if is_switch and arg_default:
            arg_name+= "=N"
        padding = ' ' * (15 - len(arg_name))
        line = f"  {arg_name}{padding}{arg_descr}"
        if arg_default:
            line += f" [Default: {arg_default}]"
        print(line)


def print_cmd_help(binary, cmd):
    print("USAGE")
    usage_line = f"{binary} {cmd.name}"
    if cmd.args:
        args = ' '.join([arg2str(x) for x in cmd.args])
        usage_line += f" {args}"
        print(f"  {binary} {cmd.name} {args}")
        print("\nARGUMENTS")
        print_args(cmd, True)
        print("\nOPTIONS")
        print_args(cmd, False)
