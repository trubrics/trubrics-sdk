from mlting.base import BaseTester


def test_feature_in_top_n_important_features(
    feature: str,
    feature_importance: dict,
    runner: str,
    top_n_features: int = 3,
):
    count = 0
    for importance in feature_importance.values():
        if importance > feature_importance.get(feature):
            count += 1
    BaseTester(count, top_n_features).assertion(type="less_equal", runner=runner)
