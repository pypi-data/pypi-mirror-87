from .semversion import SemVersion # noqa
try:
    from .version import __version__
except ImportError:
    __version__ = "0.0.0"
