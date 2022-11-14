from trubrics.context import DataContext
from trubrics.example.titanic import get_titanic_data_and_model
from trubrics.validations import ModelValidator, Trubric
from trubrics.validations.run import TrubricRun
from trubrics.validations.validation_output import validation_output


class ExampleCustomModel:
    """
    This is an example of how to wrap a custom model in the trubrics-sdk.
    """

    def __init__(self, model):
        self.model = model
        self._estimator_type = "classifier"

    def predict(self, df):
        return self.model.predict(df)

    def fit(self, X_train, y_train):
        return self.model.fit(X_train, y_train)

    def get_params(self, deep):
        return {"model": self.model}


class CustomValidator(ModelValidator):
    def __init__(self, data: DataContext, model, custom_scorers=None, slicing_functions=None):
        self.data = data
        self.model = model

    def _validate_master_age(self, age_limit_master):
        master_df = self.data.testing_data.loc[lambda df: df["Title"] == "Master"]
        errors_df = master_df.loc[lambda df: df["Age"] >= age_limit_master]
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()}

    @validation_output
    def validate_master_age(self, age_limit_master: int, severity=None):
        """Validate that passengers with the title "master" are younger than a certain age

        Args:
            age_limit_master: cut off value for master

        Returns:
            True for success, false otherwise. With a results dictionary giving dict of errors.
        """
        return self._validate_master_age(age_limit_master)

    def _validate_model_scores_females_higher(self):
        predictions_df = self.data.testing_data.assign(predictions=self.model.predict(self.data.X_test))

        def _average_score_sex(sex):
            return round(predictions_df.loc[predictions_df["Sex"] == sex, "predictions"].mean(), 3)

        score_female = _average_score_sex(sex="female")
        score_male = _average_score_sex(sex="male")
        return score_female > score_male, {"score_female": score_female, "score_male": score_male}

    @validation_output
    def validate_model_scores_females_higher(self, severity=None):
        """We want the model to score female passengers with a higher probability of survival,
        so we are validating the average scores are higher for females than for males.

        Returns:
            True for success, false otherwise. With a results dictionary giving mean scores for both populations.
        """
        return self._validate_model_scores_females_higher()

    def _validate_cv_scores(self, metric, cv, threshold_std):
        import numpy as np
        from sklearn.model_selection import cross_validate

        if self.data.training_data is None:
            raise ValueError("Training data must be specified for cross validation.")
        cv_results = cross_validate(self.model, self.data.X_train, self.data.y_train, cv=cv, scoring=metric)
        test_scores = cv_results["test_score"]
        std_test_scores = np.std(test_scores)
        return std_test_scores < threshold_std, {"test_scores": list(test_scores), "std_test_scores": std_test_scores}

    @validation_output
    def validate_cv_scores(self, metric, cv, threshold_std, severity=None):
        """
        Validate that std of CV scores is inferior to a threshold.

        TODO:
        - Check for .fit() method for custom estimators
        """
        return self._validate_cv_scores(metric, cv, threshold_std)


train_df, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    name="my_first_dataset", version=0.1, training_data=train_df, testing_data=test_df, target="Survived"
)
trubric = Trubric.parse_file("./my_first_trubric.json")

RUN_CONTEXT = TrubricRun(
    data_context=data_context,
    model=ExampleCustomModel(model),
    trubric=trubric,
    custom_validator=CustomValidator,
)
