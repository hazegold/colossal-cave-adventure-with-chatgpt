
import time

def retries(attempts: int):
    def decorator_retries(f):
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    pass
            raise Exception(f"failed after {attempts} attempts")
        return wrapper
    return decorator_retries

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