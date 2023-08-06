from cmdliner import singleton


def verbose(verbosity, message):
    if singleton.verbosity >= verbosity:
        print(message)
