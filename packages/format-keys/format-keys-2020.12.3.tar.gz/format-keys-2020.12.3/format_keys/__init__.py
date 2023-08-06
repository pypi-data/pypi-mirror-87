__all__ = ['keys']


from string import Formatter


def keys(string):
    """return a list of format keys"""
    return [fname for _, fname, _, _ in Formatter().parse(string) if fname]
