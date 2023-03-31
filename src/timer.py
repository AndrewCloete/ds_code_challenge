import time

def time_the_thing(description: str):
    def wrap1(func):
        def wrap2(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            duration = end - start
            print("%s: %.3f us" % (description, duration*1e6))
            return result
        return wrap2
    return wrap1