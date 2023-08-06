__all__ = ["slice"]


def slice(d, keys):
    """return dictionary with given keys"""
    result = dict()
    for k in keys:
        if k in d:
            result[k] = d[k]
    return result
