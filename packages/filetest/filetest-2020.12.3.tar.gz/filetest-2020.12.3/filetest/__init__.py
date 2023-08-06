__all__ = ['d', 'e', 'f', 'nt', 'ot', 'r', 's', 'x', 'w']


import os


def d(path):
    """return True if path exists and is a directory, else False"""
    return os.path.exists(path) and os.stat(path).st_size


def e(path):
    """return True if path exists, else False"""
    return os.path.exists(path)


def f(path):
    """return True if file exists and is a regular file, else False"""
    return os.path.exists(path) and os.path.isfile(path)


def nt(path1, path2):
    """return True if path1 is newer than path2, else False"""
    t1 = os.path.getmtime(path1) if os.path.exists(path1) else None
    t2 = os.path.getmtime(path2) if os.path.exists(path2) else None
    return (t1 and t2 and t1 > t2) or (t1 and not t2)


def ot(path1, path2):
    """return True if path1 is older than path2, else False"""
    t1 = os.path.getmtime(path1) if os.path.exists(path1) else None
    t2 = os.path.getmtime(path2) if os.path.exists(path2) else None
    return (t1 and t2 and t2 > t1) or (t2 and not t1)


def r(path):
    """return True if path exists and has read permission (for the current user), else False"""
    return os.path.exists(path) and os.access(path, os.R_OK)


def s(path):
    """return True if path exists and is not zero size, else False"""
    return os.path.exists(path) and os.stat(path).st_size


def x(path):
    """return True if path exists and has execute permission (for the current user), else False"""
    return os.path.exists(path) and os.access(path, os.X_OK)


def w(path):
    """return True if path exists and has write permission (for the current user), else False"""
    return os.path.exists(path) and os.access(path, os.W_OK)
