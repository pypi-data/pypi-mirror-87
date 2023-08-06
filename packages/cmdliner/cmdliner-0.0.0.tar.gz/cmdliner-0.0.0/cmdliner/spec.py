from collections import namedtuple

CommandSpec = namedtuple('Command', ['name', 'description', 'args'])


def param2dict(line: str):
    name, description = line.split(":")
    name = name.strip()
    description = description.strip()
    return {name: description}


def doc2spec(spec: str) -> CommandSpec :
    cmd_desc = None
    cmd_name = None
    args = []
    for line in spec.splitlines():
        line = line.strip("\t ")
        if not line:  # skip empty lines
            continue
        if not cmd_desc:
            cmd_desc = line
        elif not cmd_name:
            cmd_name = line
        elif cmd_name and cmd_desc:
            args.append(param2dict(line))
    return CommandSpec(cmd_name, cmd_desc, args)
