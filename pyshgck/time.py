""" Utilities to measure time. """

import time


def time_it(logger = None):
    def outer_decorator_time_it(func):
        def decorator_time_it(*args, **kwargs):
            begin_time = time.time()
            return_value = func(*args, **kwargs)
            end_time = time.time()

            exec_time = end_time - begin_time
            timing_str = "Execution time for {}: {} seconds".format(
                func.__name__, int(exec_time)
            )
            if logger:
                logger.debug(timing_str)
            else:
                print(timing_str)

            return return_value
        return decorator_time_it
    return outer_decorator_time_it
