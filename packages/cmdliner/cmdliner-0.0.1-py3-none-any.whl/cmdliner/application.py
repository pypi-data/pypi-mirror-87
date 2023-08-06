import sys
from functools import partial
from pathlib import Path
from attr import attrs, attrib
from .spec import doc2spec
from .usage_help import print_cmd_help

common_options = """
Options:
  --help        Show the help message for the application or a command
  --version     Show the application version and exit
  -v,-vv,-vvv   Verbose, very verbose, extra verbose
"""

@attrs
class Application():
    app_name = attrib()
    version = attrib()
    app_doc = attrib()
    verbosity = attrib(default=0)
    commands = attrib(default=[])
    is_help = attrib(default=False)

    def run(self):
        self.binary = sys.argv[0]
        posix_bin = Path(self.binary).as_posix()
        if posix_bin.endswith("/__main__.py"):
            module_name = Path(self.binary).parts[-2]
            self.binary = f"python -m {module_name}"

        args = self._check_common_options()
        if args is None:
            return
        if len(args) == 0:
            self._print_usage()
            if self.is_help:
                return
            else:
                exit(1)  # Missing arguments
        cmd_name = args[0]
        cmd_spec = self._find_command(cmd_name)

        if cmd_spec is None:
            print(f"'{cmd_name}' is not a supported command, list the available commands using --help")
            exit(1)

        if self.is_help:
            print_cmd_help(self.binary, cmd_spec)

    def _find_command(self, command: str):
        for cmd in self.commands:
            if cmd.name == command:
                return cmd

    def _check_common_options(self):
        COMMON_OPTS = {
            "--help": self._set_is_help,
            "--version": self._print_version,
            "-v": partial(self._set_verbose, 1),
            "-vv" : partial(self._set_verbose, 2),
            "-vvv" : partial(self._set_verbose, 3)
        }
        args = sys.argv[1:]
        options = []
        for arg_value in args:
            if arg_value[0] == '-':
                options.append(arg_value)
            else:
                break
        for option in options:
            handler = COMMON_OPTS.get(option)
            if not handler:
                print(f"{option} is not a supported option!", file=sys.stderr)
                exit(1)
            result = handler()
            if result is None:
                return None
        return args[len(options):]

    def _print_version(self):
        print(f"{self.app_name} {self.version}")

    def _print_usage(self):
        print(f"Usage: {self.binary} [OPTIONS] COMMAND")
        print(self.app_doc)
        print(common_options)
        self._print_commands()
        for cmd in self.commands:
            print(f" {cmd.name}\t\t{cmd.description}")

    def _print_commands(self):
        print("Commands:")

    def add(self, command_cls):
        self.commands.append(doc2spec(command_cls.__doc__))

    def _set_is_help(self):
        self.is_help = True
        return True

    def _set_verbose(self, verbosity):
        self.verbosity = verbosity
        return True
