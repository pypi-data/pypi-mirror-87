import sys
from pathlib import Path
from . import singleton


class cli(object):
    def __init__(self, app_version=None, app_name=None):
        if app_version is None:
            singleton.func()
        self.app_version = app_version
        self.app_name = app_name or Path(sys.argv[0]).name

    def __call__(self, func, *args, **kwargs):
        def inner_func():
            original_argv = sys.argv[:]
            singleton.verbosity = self.check_verbose_flags()
            if self.check_version():
                return
            result = func(*args, **kwargs)
            sys.argv = original_argv
            return result

        singleton.func = inner_func
        return inner_func

    def check_version(self):
        if "--version" in sys.argv:
            print(f"{self.app_name} {self.app_version}")
            return True

    def check_verbose_flags(self):

        new_args = []
        verbose_count = 0

        for arg_value in sys.argv:
            if arg_value[0] == "-" and arg_value.strip("-v") == "":
                verbose_count = arg_value.count("v")
                continue
            new_args.append(arg_value)

        sys.argv = new_args
        return verbose_count
