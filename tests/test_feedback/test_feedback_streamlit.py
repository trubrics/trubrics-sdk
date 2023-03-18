import pytest

from trubrics.integrations.streamlit import FeedbackCollector


def test_feedback_collector_raises():
    with pytest.raises(ValueError):
        FeedbackCollector(trubrics_platform_auth="something")


def test_st_auth_raises():
    collector = FeedbackCollector()
    with pytest.raises(ValueError):
        collector.st_trubrics_auth()


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"type": "thumbs"}),
        ({"type": "faces"}),
        ({"type": "issue"}),
    ],
)
def test_st_feedback_types(kwargs):
    collector = FeedbackCollector()
    collector.st_feedback(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        ({"type": "custom"}),
        ({"type": "custom", "title": "foo"}),  # no description
        ({"type": "random"}),
        ({"type": "faces", "description": "desc"}),
        ({"type": "thumbs", "description": "desc"}),
    ],
)
def test_st_feedback_raises(kwargs):
    collector = FeedbackCollector()
    with pytest.raises(ValueError):
        collector.st_feedback(**kwargs)
