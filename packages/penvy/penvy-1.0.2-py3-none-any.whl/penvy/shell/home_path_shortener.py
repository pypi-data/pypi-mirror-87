import os


def shorten_home_path(path: str):
    return path.replace(os.path.expanduser("~"), "~").replace("\\", "/")
