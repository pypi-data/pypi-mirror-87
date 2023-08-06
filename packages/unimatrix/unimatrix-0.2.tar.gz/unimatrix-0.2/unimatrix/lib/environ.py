"""Declares primitives to parse data from the operating
system environment.
"""


def parselist(environ, key, sep=':', cls=tuple):
    """Parses the environment variable into an iterable,
    using `sep` as a separator e.g.::

    >>> from unimatrix.lib.environ import parselist
    >>> parselist({'foo': '1:2'}, 'foo')
    ('1', '2')
    """
    values = environ.get(key) or ''
    return cls(filter(bool, str.split(values, sep)))
