from importlib import import_module
from warnings import warn


def load_txt(*args, **kwargs):
    return load("TXT", *args, **kwargs)


def load_bin(*args, **kwargs):
    return load("BIN", *args, **kwargs)


def load(type_, bundles="asof20201127 asof20201118".split()):
    for asof in bundles:
        try:
            mod = import_module("shukujitsu.%s" % asof)
        except ImportError as e:
            warn(repr(e), category=ImportWarning, stacklevel=2)
        else:
            return getattr(mod, type_)
    else:
        raise RuntimeError("No holidays data is available")
