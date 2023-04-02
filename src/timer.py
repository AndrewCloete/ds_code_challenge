import time

def time_the_thing(description: str):
    def wrap1(func):
        def wrap2(*args, **kwargs):
            print("Timing " + func.__name__ + "...")
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            duration = end - start
            print("%s: %.3f sec" % (description, duration))
            print()
            return result
        return wrap2
    return wrap1