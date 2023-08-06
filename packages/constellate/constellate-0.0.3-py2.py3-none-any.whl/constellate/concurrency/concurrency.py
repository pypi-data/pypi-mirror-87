from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager


@contextmanager
def new_threadpool(*args, wait=True, **kwds):
    resource = ThreadPoolExecutor(*args, **kwds)
    try:
        yield resource
    finally:
        resource.shutdown(wait=wait)


@contextmanager
def new_proceesspool(*args, wait=True, **kwds):
    resource = ProcessPoolExecutor(*args, **kwds)
    try:
        yield resource
    finally:
        resource.shutdown(wait=wait)
