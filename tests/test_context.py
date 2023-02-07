import pytest

from trubrics.context import DataContext
from trubrics.exceptions import PandasSchemaError
from trubrics.validations.dataclass import Validation


def test_data_context_attributes(dummy_testing_data):
    business_columns = {"feature 2": "feature 3"}
    dc = DataContext(testing_data=dummy_testing_data, target="target", business_columns=business_columns)

    assert dc.name == "my_dataset"
    assert dc.version == "v0.0.1"
    assert dc.features == ["feature_1", "feature 2"]
    assert all(
        [
            a == b
            for a, b in zip(
                dc.renamed_testing_data.columns, dummy_testing_data.rename(columns=business_columns).columns
            )
        ]
    )


@pytest.mark.parametrize(
    "training_data_rename_cols,kwargs,error_type",
    [
        ({"feature_1": "feature_one"}, {"target": "target"}, PandasSchemaError),
        ({}, {"target": "wrong_target"}, KeyError),
        ({}, {"categorical_columns": ["feature"]}, KeyError),
        ({}, {"categorical_columns": ["target"]}, KeyError),
        ({}, {"business_columns": {"feature 1": "feature"}}, KeyError),
        ({}, {"features": ["feature"]}, PandasSchemaError),
    ],
)
def test_data_context_raises(dummy_testing_data, training_data_rename_cols, kwargs, error_type):
    training_data = dummy_testing_data.rename(columns=training_data_rename_cols)
    with pytest.raises(error_type):
        DataContext(testing_data=dummy_testing_data, training_data=training_data, **kwargs)


@pytest.mark.parametrize(
    "kwargs,error_type",
    [
        ({"outcome": "wrong_outcome", "severity": "experiment"}, KeyError),
        ({"outcome": "pass", "severity": "wrong_severity"}, KeyError),
    ],
)
def test_validation_context_raises(kwargs, error_type):
    with pytest.raises(error_type):
        Validation(validation_type="validate_something", validation_kwargs={"a kwarg": None}, **kwargs)
