""" Utilities to measure time. """

import time


def time_it(logger = None):
    def time_it_func_decorator(func):
        def time_it_decorator(*args, **kwargs):
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
        return time_it_decorator
    return time_it_func_decorator
