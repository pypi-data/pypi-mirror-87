__all__ = ['clear', 'get', 'exists', 'rm', 'update']


import os

XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
KV_CACHE = os.getenv("KV_CACHE", os.path.join(XDG_CACHE_HOME, 'kv-cache'))


def getpath(key):
    return os.path.join(KV_CACHE, key)


def exists(key):
    """return True if key exists, else False"""
    fullpath = getpath(key)
    return os.path.exists(fullpath)


def get(key):
    """get cache value"""
    path = getpath(key)
    if os.path.exists(path):
        return open(path).read()


def update(key, string):
    """update cache value"""
    path = getpath(key)
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    open(path, "w").write(string)


def rm(key):
    """remove cache key"""
    path = getpath(key)
    if os.path.exists(path):
        os.unlink(path)


def clear():
    """remove all cache keys"""
    path = KV_CACHE
    if os.path.exists(path) and os.path.isfile(path):
        os.unlink(path)
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
