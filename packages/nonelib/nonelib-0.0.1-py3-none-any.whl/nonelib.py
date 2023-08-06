import functools


class Error(Exception):
    pass


class NoneInArgsError(Error):
    def __init__(self, none_idx, func_name):
        super().__init__(
            f"Got None as an arg #{none_idx} to {func_name};"
            f" pass it as a kwarg or wrap {func_name} with @nonewrap(none_args=True)"
        )


def nonedict(*args, **kwargs):
    return {k: v for k, v in dict(*args, **kwargs).items() if v is not None}


def nonewrap(none_args=False):

    def deco(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not none_args:
                for idx, value in enumerate(args):
                    if value is None:
                        raise NoneInArgsError(none_idx=idx, func_name=func.__name__)
            return func(*args, **nonedict(kwargs))

        return wrapper

    return deco


def noneiter(it):
    return (elem for elem in it if elem is not None)


def nonelist(lst):
    return [elem for elem in lst if elem is not None]


def noneset(set_):
    return {elem for elem in set_ if elem is not None}
