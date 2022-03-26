import hashlib


def hash(string, *, algorithm="sha256"):
    """
    returns a hash (=digest) of a provided string
    default algorithm is sha256
    """
    algo = getattr(hashlib, algorithm, None)
    if algo is None:
        raise AttributeError(f"Algorithm '{algorithm}' does not exist")
    m = algo()
    m.update(bytearray(string, encoding="utf-8"))
    return m.hexdigest()