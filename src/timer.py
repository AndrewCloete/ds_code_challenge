import time

def time_the_thing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return {"payload": result, "time": end - start}
    return wrapper