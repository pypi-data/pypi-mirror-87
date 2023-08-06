def compose(*funcs):
    *funcs, penultimate, last = funcs
    if funcs:
        penultimate = strict_compose(*funcs, penultimate)
    return lambda *args, **kwargs: penultimate(last(*args, **kwargs))

