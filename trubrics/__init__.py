from trubrics.feedback import Feedback

try:
    from importlib.metadata import version  # type: ignore
except ImportError:
    # for python<3.8
    from importlib_metadata import version  # type: ignore

__version__ = version("trubrics")

__all__ = ["Feedback"]
