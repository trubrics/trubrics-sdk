import joblib
import pandas as pd
import pytest

from examples.cli.custom_scorer import custom_scorers
from examples.cli.slicing_functions import slicing_functions
from trubrics.context import DataContext, TrubricContext
from trubrics.validations import ModelValidator


@pytest.fixture
def dummy_testing_data():
    return pd.DataFrame(
        {
            "target": [1, 2, 3],
            "feature_1": [10, 20, 30],
            "feature 2": ["a", "b", "c"],
        }
    )


@pytest.fixture
def data_context():
    testing_data = pd.read_csv("assets/tests/classifier_test_data.csv")
    training_data = pd.read_csv("assets/tests/classifier_train_data.csv")
    return DataContext(
        testing_data=testing_data,
        training_data=training_data,
        minimum_functionality_data=testing_data.iloc[:1],
        target="Survived",
    )


@pytest.fixture
def classifier_model():
    return joblib.load("assets/tests/classifier_test_model.pkl")


@pytest.fixture
def validator_classifier(data_context, classifier_model):
    return ModelValidator(
        data=data_context, model=classifier_model, custom_scorers=custom_scorers, slicing_functions=slicing_functions
    )


@pytest.fixture
def trubric():
    trubric_filename = "assets/tests/classifier_test_trubric.json"
    return TrubricContext.parse_file(trubric_filename)
