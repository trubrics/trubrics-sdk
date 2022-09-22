import timeit
from collections import defaultdict
from typing import Any, Callable, Dict, Optional, Union

import numpy as np
import pandas as pd
import sklearn.metrics
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.inspection import permutation_importance

from trubrics.context import DataContext, TrubricsModel
from trubrics.exceptions import EstimatorTypeError, SklearnMetricTypeError
from trubrics.validations.validation_output import (
    validation_output,
    validation_output_type,
)


class ModelValidator:
    def __init__(
        self,
        data: DataContext,
        model: Any,
        custom_scorers: Optional[Dict[str, Any]] = None,
        slicing_functions: Optional[Dict[str, Any]] = None,
    ):
        self.tm = TrubricsModel(data=data, model=model)
        self.model_type = self.tm.model_type
        self.custom_scorers = custom_scorers
        self.slicing_functions = slicing_functions

        # dict of computed performances {"dataset_name": {"metric_name": value}}
        self.performances: Dict[str, Dict[str, float]] = defaultdict(dict)
        # dict of feature importances {"dataset_name": {"feature_name": mean_value}}
        self.feature_importances: Dict[str, dict] = defaultdict(dict)

    @validation_output
    def validate_minimum_functionality_in_range(
        self, range_value: Union[int, float] = 0, range_inclusive: bool = True, severity: Optional[str] = None
    ):
        """Minimum functionality validation for a range output.

        Validates that a model correctly predicts all points in a given set of data, within a range of values.
        This dataset must be set in the `minimum_functionality_data` parameter of the DataContext.

        Args:
            range_value: a value that is added to and subtracted from the target value for a given prediction,
                         to create a range of possible values that the prediction should fall between.
            range_inclusive: make range inclusive (x <= prediction <= y) or exclusive (x <= prediction <= y)
            severity: severity of the validation. Can be either ['error', 'warning', 'experiment']. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving all data points where \
            the model's prediction did not fall between the range given.
        """
        return self._validate_minimum_functionality_in_range(range_value, range_inclusive=range_inclusive)

    def _validate_minimum_functionality_in_range(
        self,
        range_value: Union[int, float] = 0,
        range_inclusive: bool = True,
    ) -> validation_output_type:
        if self.model_type == "classifier":
            raise EstimatorTypeError(
                "Validation may only be applied to regressor model types."
                " Try 'validate_minimum_functionality' validation for classifier model types."
            )

        minimum_functionality_df = self.tm.data.minimum_functionality_data
        if minimum_functionality_df is None:
            raise ValueError("Specify minimum_functionality_data attribute in DataContext.")

        def filter_predictions_not_in_range(minimum_functionality_df, range_value, range_inclusive):
            if range_inclusive:
                return minimum_functionality_df.loc[
                    lambda x: (x["predictions"] >= x[self.tm.data.target] + range_value)
                    | (x["predictions"] <= x[self.tm.data.target] - range_value),
                    :,
                ]
            else:
                return minimum_functionality_df.loc[
                    lambda x: (x["predictions"] > x[self.tm.data.target] + range_value)
                    | (x["predictions"] < x[self.tm.data.target] - range_value),
                    :,
                ]

        minimum_functionality_df["predictions"] = self.tm.predictions_minimum_functionality
        errors_df = filter_predictions_not_in_range(minimum_functionality_df, range_value, range_inclusive)
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()} if len(errors_df) != 0 else {}

    @validation_output
    def validate_minimum_functionality(self, severity: Optional[str] = None):
        """Minimum functionality validation.

        Validates that a model correctly predicts all points in a given set of data. This dataset must be set
        in the `minimum_functionality_data` parameter of the DataContext.

        Args:
            severity: severity of the validation. Can be either ['error', 'warning', 'experiment']. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving all data points that were not \
            correctly predicted by the model.
        """
        return self._validate_minimum_functionality()

    def _validate_minimum_functionality(self) -> validation_output_type:
        if self.model_type == "regressor":
            raise EstimatorTypeError(
                "Validation may only be applied to classifier model types."
                " Try 'validate_minimum_functionality_in_range' validation for regressor model types."
            )
        minimum_functionality_df = self.tm.data.minimum_functionality_data
        if minimum_functionality_df is None:
            raise ValueError("Specify minimum_functionality_data attribute in DataContext.")
        minimum_functionality_df["predictions"] = self.tm.predictions_minimum_functionality
        errors_df = minimum_functionality_df.loc[lambda x: x[self.tm.data.target] != x["predictions"], :]
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()} if len(errors_df) != 0 else {}

    @validation_output
    def validate_performance_against_threshold(
        self,
        metric: str,
        threshold: float,
        dataset: str = "testing_data",
        data_slice: Optional[str] = None,
        severity: Optional[str] = None,
    ):
        """Performance validation versus a fixed threshold value.

        Compares performance of a model on any of the datasets in the DataContext to a hard coded threshold value.

        Args:
            metric: performance metric name defined in sklearn (sklearn.metrics.SCORERS) or in a \
                    custom scorer fed in when initialising the ModelValidator object.
            threshold: the performance threshold that the model must attain.
            dataset: the name of a dataset from the DataContext {'testing_data', 'training_data'}.
            data_slice: the name of the data slice, specified in the slicing_functions parameter of ModelValidator.
            severity: severity of the validation. Can be either {'error', 'warning', 'experiment'}. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual model performance calculated.
        """
        return self._validate_performance_against_threshold(metric, threshold, dataset, data_slice)

    def _validate_performance_against_threshold(
        self, metric: str, threshold: float, dataset: str = "testing_data", data_slice: Optional[str] = None
    ) -> validation_output_type:
        performance = self._score_data_context(metric, dataset, data_slice)
        return bool(performance > threshold), {"performance": performance}

    @validation_output
    def validate_biased_performance_across_category(
        self, metric: str, category: str, threshold: float, severity: Optional[str] = None
    ):
        """Biased performance validation on a category.

        Calculates various performance for all values in a category and validates for
        the maximum difference in performance inferior to the threshold value.

        Args:
            metric: performance metric name defined in sklearn (sklearn.metrics.SCORERS) or in a \
                    custom scorer fed in when initialising the ModelValidator object.
            category: categorical feature to split data on
            threshold: maximum difference in performance
            severity: severity of the validation. Can be either ['error', 'warning', 'experiment']. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving the maximum performance difference.
        """
        return self._validate_biased_performance_across_category(metric, category, threshold)

    def _validate_biased_performance_across_category(
        self, metric: str, category: str, threshold: float
    ) -> validation_output_type:
        """
        TODO:
            - More complex threshold function
            - Modify cardinality

            To add to output report:

            - Performance across all category values
            - Show distributions of category variables
            - Performance plots of results
        """
        scorer = self._scorer(metric)
        test_data = self.tm.data.testing_data
        cat_values = list(test_data[category].unique())
        if len(cat_values) > 20:
            raise ValueError(f"Cardinality of {len(cat_values)} too high for performance test.")
        if len(cat_values) < 1:
            raise ValueError(f"Category '{category}' has a single value.")
        if category not in test_data.columns:
            # TODO: check when categorical columns are specified
            raise KeyError(f"Column '{category}' not found in dataset.")
        result: Dict[str, Union[int, float]] = {}
        for value in cat_values:
            if value not in [np.nan, None]:
                value = f"'{value}'" if isinstance(value, str) else value
                filtered_data = test_data.query(f"`{category}`=={value}")
                result[value] = scorer(
                    self.tm.model,
                    filtered_data.loc[:, self.tm.data.features],
                    filtered_data[self.tm.data.target],
                )
        max_performance_difference = max(result.values()) - min(result.values())

        return max_performance_difference < threshold, {"max_performance_difference": max_performance_difference}

    @validation_output
    def validate_performance_against_dummy(
        self,
        metric: str,
        strategy: str = "most_frequent",
        dummy_kwargs: Optional[dict] = None,
        data_slice: Optional[str] = None,
        severity: Optional[str] = None,
    ):
        """Performance validation versus a dummy baseline model.

        Trains a DummyClassifier / DummyRegressor from \
        [sklearn](https://scikit-learn.org/stable/modules/classes.html?highlight=dummy#module-sklearn.dummy)\
        and compares performance against the model.

        Args:
            metric: performance metric name defined in sklearn (sklearn.metrics.SCORERS) or in a \
                    custom scorer fed in when initialising the ModelValidator object.
            strategy: strategy of scikit-learns dummy model.
            dummy_kwargs: kwargs to be passed to dummy model.
            data_slice: the name of the data slice, specified in the slicing_functions parameter of ModelValidator.
            severity: severity of the validation. Can be either ['error', 'warning', 'experiment']. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving the model's \
            actual performance on the test set and the dummy model's performance.
        """
        return self._validate_performance_against_dummy(metric, strategy, dummy_kwargs, data_slice)

    def _validate_performance_against_dummy(
        self, metric: str, strategy: str, dummy_kwargs: Optional[dict] = None, data_slice: Optional[str] = None
    ) -> validation_output_type:
        test_performance = self._score_data_context(metric, dataset="testing_data", data_slice=data_slice)
        scorer = self._scorer(metric)
        if self.tm.data.training_data is None:
            raise TypeError("In order to train dummy classifier, training_data must be set in the DataContext.")

        if self.model_type == "classifier":
            Dummy = DummyClassifier
        elif self.model_type == "regressor":
            Dummy = DummyRegressor
        else:
            raise NotImplementedError()
        if dummy_kwargs:
            dummy_model = Dummy(strategy=strategy, **dummy_kwargs)
        else:
            dummy_model = Dummy(strategy=strategy)

        if data_slice:
            X_train, y_train = self._slice_data_with_slicing_function(self.tm.data.training_data, data_slice)
            X_test, y_test = self._slice_data_with_slicing_function(self.tm.data.testing_data, data_slice)
        else:
            X_train, y_train = self.tm.data.X_train, self.tm.data.y_train
            X_test, y_test = self.tm.data.X_test, self.tm.data.y_test

        dummy_model.fit(X_train, y_train)
        dummy_performance = scorer(dummy_model, X_test, y_test)

        return test_performance > dummy_performance, {
            "dummy_performance": dummy_performance,
            "test_performance": test_performance,
        }

    @validation_output
    def validate_performance_between_train_and_test(
        self,
        metric: str,
        threshold: Union[int, float],
        data_slice: Optional[str] = None,
        severity: Optional[str] = None,
    ):
        """Performance validation comparing training and test data scores.

        Scores the test set and the train set in the DataContext, and validates whether the test score is \
        inferior to but also within a certain range of the train score. Can be used to validate for overfitting
        on the training set.

        Args:
            metric: performance metric name defined in sklearn (sklearn.metrics.SCORERS) or in a \
                      custom scorer fed in when initialising the ModelValidator object.
            threshold: a positive value representing the maximum allowable difference between the train and \
                         test score.
            data_slice: the name of the data slice, specified in the slicing_functions parameter of ModelValidator.
            severity: severity of the validation. Can be either ['error', 'warning', 'experiment']. \
                      If None, defaults to 'error'.

        Returns:
            True for success, false otherwise. With a results dictionary giving the model's \
            performance on test and train sets.
        """
        return self._validate_performance_between_train_and_test(metric, threshold, data_slice)

    def _validate_performance_between_train_and_test(
        self,
        metric: str,
        threshold: Union[int, float],
        data_slice: Optional[str] = None,
    ) -> validation_output_type:
        test_score = self._score_data_context(metric, dataset="testing_data", data_slice=data_slice)
        train_score = self._score_data_context(metric, dataset="training_data", data_slice=data_slice)

        outcome = test_score < train_score and test_score >= train_score - threshold
        return outcome, {"train_score": train_score, "test_score": test_score}

    @validation_output
    def validate_inference_time(self, threshold: float, n_executions: int = 100, severity: Optional[str] = None):
        """Validate the model's inference time on a single data point from the test set.

        Args:
            threshold: number of seconds that the model inference time should be inferior to
            n_executions: number of executions of the `.predict()` method for a single data point

        Returns:
            True for success, false otherwise. With a results dictionary giving the model's \
            average inference time (in seconds).
        """
        return self._validate_inference_time(threshold, n_executions)

    def _validate_inference_time(self, threshold: float, n_executions: int = 100) -> validation_output_type:
        single_data_point = self.tm.data.X_test.iloc[[0]]
        inference_time = (
            timeit.timeit(lambda: self.tm.model.predict(single_data_point), number=n_executions) / n_executions
        )
        return inference_time < threshold, {"inference_time": inference_time}

    @validation_output
    def validate_feature_in_top_n_important_features(
        self,
        dataset: str,
        feature: str,
        top_n_features: int,
        permutation_kwargs: Optional[Dict[str, Any]] = None,
        severity: Optional[str] = None,
    ):
        """Feature importance validation for top n features.

        Validates that a given feature is in the top n most important features. For calculation of feature \
        importance we are using sklearn's [permutation_importance](https://scikit-learn.org/stable/\
        modules/generated/sklearn.inspection.permutation_importance.html#sklearn.inspection.permutation_importance).

        Args:
            dataset: the name of a dataset from the DataContext to calculate feature importance on \
                {'testing_data', 'training_data'}.
            feature: feature to assess.
            top_n_features: the number of most important features that the named feature must be ranked in. E.g. if
                            top_n_features=2, the feature must be within the top two most important features.
            permutation_kwargs: kwargs to pass into the sklearn.inspection.permutation_importance function.

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual feature importance ranking.
        """
        return self._validate_feature_in_top_n_important_features(dataset, feature, top_n_features, permutation_kwargs)

    def _validate_feature_in_top_n_important_features(
        self, dataset: str, feature: str, top_n_features: int, permutation_kwargs: Optional[Dict[str, Any]] = None
    ) -> validation_output_type:
        count = 0
        feature_importance = self._compute_permutation_feature_importance(
            dataset=dataset, permutation_kwargs=permutation_kwargs
        )
        importances_mean = feature_importance["importances_mean"]
        feature_index = self.tm.data.features.index(feature)
        for importance in importances_mean:
            if importance > importances_mean[feature_index]:
                count += 1

        feature_importances_dict = {
            key: value for key, value in zip(self.tm.data.features, feature_importance["importances_mean"])
        }
        return count < top_n_features, {
            "feature_importance_ranking": count,
            "feature_importance": feature_importances_dict,
        }

    @validation_output
    def validate_feature_importance_between_train_and_test(
        self, top_n_features: Optional[int] = None, permutation_kwargs: Optional[Dict[str, Any]] = None
    ):
        """Permutation feature importance comparison between train and test sets.

        Validates that the ranking of top n features is the same for both test and train sets. For calculation of \
        feature importance we are using sklearn's [permutation_importance](https://scikit-learn.org/stable/modules\
        /generated/sklearn.inspection.permutation_importance.html#sklearn.inspection.permutation_importance).

        Args:
            top_n_features: the number of most important features to consider for comparison between train and test \
                            sets. E.g. if top_n_features=2, the train and test sets must have the same 2 most \
                            important features, in the same order.
            permutation_kwargs: kwargs to pass into the sklearn.inspection.permutation_importance function.

        Returns:
            True for success, false otherwise. With a results dictionary giving the actual feature importance ranking.
        """
        return self._validate_feature_importance_between_train_and_test(top_n_features, permutation_kwargs)

    def _validate_feature_importance_between_train_and_test(
        self, top_n_features: Optional[int] = None, permutation_kwargs: Optional[Dict[str, Any]] = None
    ) -> validation_output_type:
        train_fi = self._compute_permutation_feature_importance(
            dataset="testing_data", permutation_kwargs=permutation_kwargs
        )
        test_fi = self._compute_permutation_feature_importance(
            dataset="training_data", permutation_kwargs=permutation_kwargs
        )
        ordered_train_fi = {
            value: key for key, value in sorted(zip(train_fi["importances_mean"], self.tm.data.features))
        }
        ordered_test_fi = {value: key for key, value in sorted(zip(test_fi["importances_mean"], self.tm.data.features))}

        if top_n_features:
            top_n_features = -top_n_features

        is_same_order = [feature for feature in ordered_train_fi][top_n_features:] == [
            feature for feature in ordered_test_fi
        ][top_n_features:]
        return is_same_order, {
            "training_feature_importance": ordered_train_fi,
            "testing_feature_importance": ordered_test_fi,
        }

    def _scorer(self, metric: str) -> Callable[[Any, pd.DataFrame, pd.Series], float]:
        if metric in sklearn.metrics.SCORERS:
            scorer = sklearn.metrics.SCORERS[metric]
        else:
            if self.custom_scorers is not None and metric in self.custom_scorers:
                scorer = self.custom_scorers[metric]
            else:
                raise SklearnMetricTypeError(
                    f"The metric '{metric}' is not part of scikit-learns scorers, nor is it defined as a custom scorer"
                    " in the custom_scorers attribute. Run `sklearn.metrics.SCORERS` to list default scorers, or input"
                    " your custom scorer to the ModelValidator."
                )
        return scorer

    def _slice_data_with_slicing_function(self, df: pd.DataFrame, data_slice: str):
        if self.slicing_functions:
            if data_slice in self.slicing_functions:
                sliced_data = self.slicing_functions[data_slice](df)
            else:
                raise ValueError(
                    f"Slice '{data_slice}' does not exist in the slicing_functions parameter of the ModelValidator."
                )
        else:
            raise TypeError(
                "In order to use data slices, add all slicing functions to the slicing_functions parameter of the"
                " ModelValidator."
            )
        return sliced_data.loc[:, self.tm.data.features], sliced_data.loc[:, self.tm.data.target]

    def _score_data_context(self, metric: str, dataset: str, data_slice: Optional[str]) -> float:
        previously_computed_performance = self.performances.get(dataset, {}).get(metric)
        if previously_computed_performance:
            return previously_computed_performance

        scorer = self._scorer(metric)
        model = self.tm.model
        if data_slice:
            X, y = self._slice_data_with_slicing_function(getattr(self.tm.data, dataset), data_slice)
            dataset = f"{dataset}_{data_slice}"
        elif data_slice is None and dataset == "testing_data":
            X, y = self.tm.data.X_test, self.tm.data.y_test
        elif data_slice is None and dataset == "training_data":
            if self.tm.data.X_train is None or self.tm.data.y_train is None:
                raise ValueError("Training data not specified in DataContext.")
            else:
                X, y = self.tm.data.X_train, self.tm.data.y_train
        else:
            raise ValueError(
                "Method reserved for testing on datasets within the DataContext: {'testing_data', 'training_data'}."
            )
        self.performances[dataset][metric] = scorer(model, X, y)
        return self.performances[dataset][metric]

    def _compute_permutation_feature_importance(
        self, dataset: str, permutation_kwargs: Optional[Dict[str, Any]]
    ) -> dict:
        previously_computed_importance = self.feature_importances.get(dataset)
        if previously_computed_importance:
            return previously_computed_importance

        if permutation_kwargs is None:
            permutation_kwargs = {"random_state": 88, "n_jobs": -1}

        if dataset == "testing_data":
            self.feature_importances[dataset] = dict(
                permutation_importance(self.tm.model, self.tm.data.X_test, self.tm.data.y_test, **permutation_kwargs)
            )
        elif dataset == "training_data":
            if self.tm.data.X_train is None or self.tm.data.y_train is None:
                raise ValueError("Training data not specified in DataContext.")
            else:
                self.feature_importances[dataset] = dict(
                    permutation_importance(
                        self.tm.model, self.tm.data.X_train, self.tm.data.y_train, **permutation_kwargs
                    )
                )
        else:
            raise ValueError(
                "Method reserved for testing on datasets within the DataContext: {'testing_data', 'training_data'}."
            )
        return self.feature_importances[dataset]
