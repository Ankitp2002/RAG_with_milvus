from functools import wraps

def handle_err_and_raise(func):
    @wraps(func)
    def inner_wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            # Raise a new error with your custom message, preserving the original track
            raise RuntimeError(f"Pipeline crashed during execution of '{func.__name__}': {err}") from err
    return inner_wraps

def handle_err_and_log(func):
    @wraps(func)
    def inner_wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            # Raise a new error with your custom message, preserving the original track
            print(f"Pipeline crashed during execution of '{func.__name__}': {err}")
            
    return inner_wraps
