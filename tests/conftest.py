import joblib
import pandas as pd
import pytest

from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.modellers.classifier import Classifier
from trubrics.validators.base import Validator


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
def data_context():
    testing_data = pd.read_csv("assets/tests/classifier_test_data.csv")
    return DataContext(testing_data=testing_data, target_column="Survived")


@pytest.fixture
def classifier_model_context():
    from sklearn.metrics import accuracy_score

    model = joblib.load("assets/tests/classifier_test_model.pkl")
    return ModelContext(estimator=model, evaluation_function=accuracy_score)


@pytest.fixture
def validator_classifier(data_context, classifier_model_context):
    trubrics_model = Classifier(data=data_context, model=classifier_model_context)
    return Validator(trubrics_model=trubrics_model)


@pytest.fixture
def trubric():
    return TrubricContext.parse_file("assets/tests/classifier_test_trubric.json")
