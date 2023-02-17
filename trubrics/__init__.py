try:
    from importlib.metadata import version
except ImportError:
    # for python<3.8
    from importlib_metadata import version

__version__ = version("trubrics")  # type: ignore
