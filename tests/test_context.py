import pandas as pd
import pytest

from trubrics.context import DataContext


@pytest.fixture
def testing_data():
    return pd.DataFrame(
        {
            "target": [1, 2, 3],
            "feature_1": [10, 20, 30],
            "feature 2": ["a", "b", "c"],
        }
    )


def test_data_context_features(testing_data):
    business_columns = {"feature 2": "feature 3"}
    dc = DataContext(testing_data=testing_data, target_column="target", business_columns=business_columns)
    assert dc.name == "my_dataset"
    assert dc.version == 0.1
    assert dc.features == ["feature_1", "feature 2"]
    assert all(
        [a == b for a, b in zip(dc.renamed_testing_data.columns, testing_data.rename(columns=business_columns).columns)]
    )
