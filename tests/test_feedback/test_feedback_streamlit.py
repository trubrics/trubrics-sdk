import pytest

from trubrics.integrations.streamlit import FeedbackCollector


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"feedback_type": "random"}),
        ({"feedback_type": "issue", "open_feedback_label": "test"}),
    ],
)
def test_st_feedback_raises(kwargs):
    collector = FeedbackCollector(project="random", email=None, password=None)
    with pytest.raises(ValueError):
        kwargs["component"] = "a component"
        kwargs["model"] = "a model"
        collector.st_feedback(**kwargs)
