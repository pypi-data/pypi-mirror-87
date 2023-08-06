__all__ = ['popd']


from functools import wraps
import os


def popd(func):
    """`@popd` decorator. restore previous current directory"""
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            cwd = os.getcwd()
            return func(*args, **kwargs)
        finally:
            os.chdir(cwd)
    return decorated
