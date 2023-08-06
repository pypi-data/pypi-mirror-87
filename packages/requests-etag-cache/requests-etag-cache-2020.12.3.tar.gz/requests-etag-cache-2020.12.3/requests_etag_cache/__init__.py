__all__ = ['clear', 'get', 'save', 'uptodate', 'rm']


import hashlib
import os
import shutil

XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
_REQUESTS_ETAG_CACHE = os.path.join(XDG_CACHE_HOME, 'requests-etag-cache')
REQUESTS_ETAG_CACHE = os.getenv("REQUESTS_ETAG_CACHE", _REQUESTS_ETAG_CACHE)


def gethash(string):
    hash_object = hashlib.sha256(string.encode())
    return hash_object.hexdigest()


def getpath(response):
    return os.path.join(REQUESTS_ETAG_CACHE, gethash(response.url))


def get(response):
    """get cached etag value"""
    path = getpath(response)
    if os.path.exists(path):
        return open(path).read()


def save(response):
    """save response etag value"""
    path = getpath(response)
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    etag = response.headers.get('etag', None)
    open(path, "w").write(str(etag))


def uptodate(response):
    """return True if response is cached, else False"""
    return get(response) == response.headers.get('etag', None)


def rm(response):
    """remove response cache"""
    path = getpath(response)
    if os.path.exists(path):
        os.unlink(path)


def clear():
    """remove all cache keys"""
    path = REQUESTS_ETAG_CACHE
    if os.path.exists(path) and os.path.isfile(path):
        os.unlink(path)
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
