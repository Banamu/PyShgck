""" Helpers for concurrency and threading stuff. """

import threading


def simple_thread(func, daemon=True):
    """ Start function in another thread, discarding return value. """
    thread = threading.Thread(target=func)
    thread.daemon = daemon
    thread.start()
    return thread
