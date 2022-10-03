# The DataContext

Data sits at the heart of all ML projects, thus also playing a central role in using the trubrics-sdk. We have decided to group all ML datasets and metadata into a single object: the `DataContext`. Initialising this object is the first step to both [building validations with `ModelValidator`](validations.md) and [collecting user feedback with the `FeedbackCollector`](feedback.md).

## Getting started with the DataContext
The most basic level of ML validation can be performed on **a single dataset** (of data that has not been seen during model training) and **a single model**. This `testing_data` dataset must contain:

- all features that were used to train the model (no extra columns permitted)
- the target variable to predict

This is the minimum requirement for the `DataContext` to start building validations:

!!!example

    ```py
    from trubrics.context import DataContext
    data_context = DataContext(
        testing_data=test_df,  # pandas dataframe of data to validate model on
        target="target_variable",  # name of target variable within the testing_data dataset
    )
    ```

There are many other attributes to the `DataContext` that can be used in validations / collecting feedback:

!!!tip "DataContext object"
    :::trubrics.context.DataContext

## DataContext versioning
Versioning the different datasets in a `DataContext` is currently left to the developer. There are `name` and `version` attributes that will allow the tracking of the `DataContext` throughout, eventually being fed into a [saved `Trubric`](save_trubric.md) .json file.

!!!example

    ```py
    from trubrics.context import DataContext
    data_context = DataContext(
        name="titanic",
        version=0.3,
        testing_data=test_df,
        target="target_variable",
    )
    ```

## Training & Minimum Functionality datasets
There are two additional datasets that can be used in the `DataContext` for different [validations](validations.md):

- `training_data`: can be used interchangeably with `testing_data` in most [performance](validations.md#performance) or [feature importance](validations.md#feature-importance) validations. 
- `minimum_functionality_data`: for [minimum functionality](validations.md#minimum-functionality) validations.

!!!example

    ```py
    from trubrics.context import DataContext
    data_context = DataContext(
        testing_data=test_df,
        target="target_variable",
        training_data=train_df,
        minimum_functionality_data=minimum_functionality_df,
    )
    ```

## Data features metadata
There are two extra attributes that hold metadata for the [FeedbackCollector](feedback.md):

- `categorical_columns`: used for distinguishing between different input widgets in the what-if component
- `business_columns`: used for renaming dataset columns with a different name for business user understanding

!!!example

    ```py
    from trubrics.context import DataContext
    data_context = DataContext(
        testing_data=test_df,
        target="target_variable",
        categorical_columns=["feature_a", "feature_b"],
        business_columns={"feature_a": "renamed_feature_a"},
    )
    ```
