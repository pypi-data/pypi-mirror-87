#!/usr/bin/env python


def deep_merge(a, b, level=0, max_depth=9):
    """Deep merge 2 dicts a and b

    Dict b is merged into dict a. If a and b have the same key on the same
    level, b's value override a's.

    The maximum recusive depth is 9 by default.
    """

    if level >= max_depth:
        return b
    else:
        level += 1

    # If neither a nor b is dict, no need to check further.
    if not isinstance(a, dict):
        return b
    if not isinstance(b, dict):
        return b

    for key in b:
        if key in a:
            a[key] = deep_merge(a[key], b[key], level=level, max_depth=max_depth)
        else:
            a[key] = b[key]

    return a
