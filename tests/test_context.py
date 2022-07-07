import pandas as pd
import pytest

from trubrics.context import DataContext, ModelContext, ValidationContext
from trubrics.exceptions import PandasSchemaError


@pytest.fixture
def testing_data():
    return pd.DataFrame(
        {
            "target": [1, 2, 3],
            "feature_1": [10, 20, 30],
            "feature 2": ["a", "b", "c"],
        }
    )


def test_data_context_attributes(testing_data):
    business_columns = {"feature 2": "feature 3"}
    dc = DataContext(testing_data=testing_data, target_column="target", business_columns=business_columns)

    assert dc.name == "my_dataset"
    assert dc.version == 0.1
    assert dc.features == ["feature_1", "feature 2"]
    assert all(
        [a == b for a, b in zip(dc.renamed_testing_data.columns, testing_data.rename(columns=business_columns).columns)]
    )


@pytest.mark.parametrize(
    "training_data_rename_cols,kwargs,error_type",
    [
        ({"feature_1": "feature_one"}, {"target_column": "target"}, PandasSchemaError),
        ({}, {"target_column": "wrong_target"}, KeyError),
        ({}, {"categorical_columns": ["feature"]}, KeyError),
        ({}, {"categorical_columns": ["target"]}, Exception),
        ({}, {"business_columns": {"feature 1": "feature"}}, KeyError),
    ],
)
def test_data_context_raises(testing_data, training_data_rename_cols, kwargs, error_type):
    training_data = testing_data.rename(columns=training_data_rename_cols)
    with pytest.raises(error_type):
        DataContext(testing_data=testing_data, training_data=training_data, **kwargs)


def test_model_context():
    class Estimator:
        pass

    class EvalFunction:
        def __name__(self):
            return "EvalFunction"

    mc = ModelContext(name="my_new_model", estimator=Estimator, evaluation_function=EvalFunction)

    assert mc.name == "my_new_model"
    assert mc.version == 0.1
    assert mc.evaluation_function_name == "EvalFunction"


@pytest.mark.parametrize(
    "kwargs,error_type",
    [
        ({"outcome": "wrong_outcome", "severity": "experiment"}, KeyError),
        ({"outcome": "pass", "severity": "wrong_severity"}, KeyError),
    ],
)
def test_validation_context_raises(kwargs, error_type):
    with pytest.raises(error_type):
        ValidationContext(validation_type="validate_something", validation_kwargs={"a kwarg": None}, **kwargs)
