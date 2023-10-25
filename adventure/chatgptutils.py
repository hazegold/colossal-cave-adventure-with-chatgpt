
import time

def ratelimited(interval: int):
    def decorator_ratelimited(f):
        last = -interval
        def wrapper(*args, **kwargs):
            nonlocal last
            current = time.time()
            elapsed = current - last
            last = current
            if elapsed < interval:
                time.sleep(interval - elapsed) 
            return f(*args, **kwargs)
        return wrapper
    return decorator_ratelimited

# TODO: Factor out logging utilities here