# Metrics and scoring functions

!!!warning "trubrics>1.4.2"
    Validations in Trubrics will soon be moved to another repository. For trubrics>1.4.2 users, please install all validations dependencies with:
    ```
    pip install "trubrics[validations]"
    ```

Many validations in the `ModelValidator` require the computation of a metric to validate. It is good practice to recompute these metrics outside of your training pipeline to avoid errors in passing on pre-computed metrics. As performance computation can be expensive in compute, a given metric is calculated once on a given dataset, and stored in the `ModelValidator` for use by any following validations. The dataset can be any datasets present in the [DataContext](data_context.md), or any [slices](#3-data-slicing-functions) of these datasets.

!!!example
    For example, here the `ModelValidator` computes recall on the test set for the first validation, and then uses this stored value in the second validation.
    ```py
    from trubrics.validations import ModelValidator
    model_validator = ModelValidator(data=data_context, model=model)
    validations = [
        model_validator.validate_test_performance_against_dummy(metric="recall", strategy="stratified")
        model_validator.validate_performance_between_train_and_test(metric="recall", threshold=0.3)
    ]
    print(model_validator.performances)  # all performance values are stored in the performances attribute
    ```

## 1. Scikit-learn scoring functions
The `ModelValidator` makes use of [sklearn.metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics) to compute model performance on a given dataset. The metric is fed into the validation as a string (as above), to use any of sklearn's scorers. 

!!!note
    List available scorers by running:
    ```py
    import sklearn.metrics
    print(sklearn.metrics.SCORERS)
    ```

## 2. Custom scoring functions
To create your own scoring functions, scikit-learn provides a [make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html#sklearn.metrics.make_scorer) function. In the case of an error metric, where a lower value is better, make use of the `greater_is_better=False` argument in order to stay consistent with comparison of metrics in performance validations.

!!!example
    Here is an example of a custom scoring function being fed into the `ModelValidator` and used in a performance validation:
    ```py
    from trubrics.validations import ModelValidator
    ---8<-- "examples/validations/classification_titanic/custom_scorer.py"
    
    model_validator = ModelValidator(data=data_context, model=model, custom_scorers=custom_scorers)
    validations = [
        model_validator.validate_test_performance_against_dummy(metric="my_custom_loss", strategy="stratified")
    ]
    ```

## 3. Data slicing functions
It is often necessary to compute performance on specific splits of a dataset, in order to test for model performance bias for example. Data slicing functions can also be fed into the `ModelValidator`, and used in validations in the same way that metrics are. Each function must take a single pandas dataframe argument, and return the filtered pandas dataframe.

!!!example
    Here is an example of a series of data slicing functions being fed into the `ModelValidator` and used in a validation:
    ```py
    from trubrics.validations import ModelValidator
    ---8<-- "examples/validations/classification_titanic/slicing_functions.py"
    
    model_validator = ModelValidator(
        data=data_context, model=model, slicing_functions=slicing_functions
    )

    validations = [
        model_validator.validate_test_performance_against_dummy(
            metric="accuracy", strategy="stratified", data_slice="female"
        )
    ]
    ```
