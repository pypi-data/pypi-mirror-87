from shutil import which


def is_executable(name):
    return which(name) is not None
