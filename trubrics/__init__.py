from trubrics.feedback import Feedback
from trubrics.feedback import save_to_trubrics as save
from trubrics.integrations import FeedbackCollector
from trubrics.trubrics_platform import init

try:
    from importlib.metadata import version  # type: ignore
except ImportError:
    # for python<3.8
    from importlib_metadata import version  # type: ignore

__version__ = version("trubrics")

__all__ = ["Feedback", "FeedbackCollector", "init", "save"]
