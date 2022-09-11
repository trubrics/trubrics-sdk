import json

import joblib
import pandas as pd
import pytest

from trubrics.context import DataContext, TrubricContext
from trubrics.validations import ModelValidator


@pytest.fixture
def testing_data():
    return pd.DataFrame(
        {
            "target": [1, 2, 3],
            "feature_1": [10, 20, 30],
            "feature 2": ["a", "b", "c"],
        }
    )


@pytest.fixture
def feature_importance():
    with open("assets/tests/test_feature_importance.json", "r") as file:
        return json.loads(file.read())


@pytest.fixture
def data_context():
    testing_data = pd.read_csv("assets/tests/classifier_test_data.csv")
    training_data = pd.read_csv("assets/tests/classifier_train_data.csv")
    return DataContext(testing_data=testing_data, training_data=training_data, target_column="Survived")


@pytest.fixture
def classifier_model():
    return joblib.load("assets/tests/classifier_test_model.pkl")


@pytest.fixture
def validator_classifier(data_context, classifier_model):
    return ModelValidator(metric="accuracy", data=data_context, model=classifier_model)


@pytest.fixture
def trubric():
    trubric_filename = "assets/tests/classifier_test_trubric.json"
    return TrubricContext.parse_file(trubric_filename)
