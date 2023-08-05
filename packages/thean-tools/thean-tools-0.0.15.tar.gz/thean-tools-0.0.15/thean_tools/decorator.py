import threading
import time
from logzero import logger


def print_run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        thread_name = threading.current_thread().name
        logger.info('[%s][%s]: %.3f ms' % (thread_name, func.__name__, (end - start)*1000))
        return res
    return wrapper


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func

