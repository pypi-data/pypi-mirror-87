__all__ = ['lowerdict']


def lowerdict(*args, **kwargs):
    """return dict with lowercase keys"""
    inputdict = dict(*args, **kwargs)
    resultdict = dict()
    for key, value in inputdict.items():
        try:
            resultdict[key.lower()] = value
        except AttributeError:
            resultdict[key] = value
    return resultdict
