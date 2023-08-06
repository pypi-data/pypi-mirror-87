__all__ = ['getdirs']


import os


def _iter_dirs(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            yield os.path.join(root, d)


def getdirs(path):
    """return a list of all dirs in the directory and subdirectories"""
    return list(_iter_dirs(path))
