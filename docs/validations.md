# Out-of-the-box model validations
The trubrics library comes with [out-of-the-box validations](validations.md) that you can test against your models in a
couple of lines of code. These validations are held in the `ModelValidator` object, that can be instantiated
with a [DataContext](data_context.md) and a [model](models.md). This object can also be used to build [custom validations](custom_validations.md).

## Minimum Functionality
:::trubrics.validations.ModelValidator.validate_minimum_functionality
----
:::trubrics.validations.ModelValidator.validate_minimum_functionality_in_range
----

## Performance
:::trubrics.validations.ModelValidator.validate_performance_against_threshold
----
:::trubrics.validations.ModelValidator.validate_test_performance_against_dummy
----
:::trubrics.validations.ModelValidator.validate_performance_between_train_and_test
----
:::trubrics.validations.ModelValidator.validate_performance_std_across_slices
----

## Inference time
:::trubrics.validations.ModelValidator.validate_inference_time
----

## Feature Importance
Feature importance calculation for the following validations is based on sklearn's [permutation_importance](https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html#sklearn.inspection.permutation_importance).

:::trubrics.validations.ModelValidator.validate_feature_in_top_n_important_features
----
:::trubrics.validations.ModelValidator.validate_feature_importance_between_train_and_test
----
