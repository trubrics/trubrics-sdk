# Welcome to the trubrics-sdk
-------

<center>

![logo-gradient](./assets/logo-gradient.png)

[trubrics.com](https://www.trubrics.com/home)

*Investigate models, collaborate across teams, validate machine learning.*
</center>

-------

The trubrics-sdk is a python library for validating machine learning with data science and domain expertise. This is achieved by collecting business user feedback, creating actionable validation points by combining the feedback with data science knowledge, and building repeatable validation checklists - a trubric.

## Key Features
- Python web development components (e.g. with [Streamlit](https://streamlit.io/)) to gather feedback from business users on models with the **trubrics FeedbackCollector**.
- Out of the box & custom validations (python functions) to build around models & datasets with the **trubrics ModelValidator** (currently supporting tabular data).
- **Trubrics CLI** tool to run a list of saved validations (a **trubric**) against new models or datasets in a CI/CD/CT pipeline.
<center>

![trubrics-explain](./assets/trubrics-explain.png)
</center>

## Install (Python 3.7+)
```console
(venv)$ pip install trubrics
```

## Initialise a DataContext
The `DataContext` wraps ML datasets and metadata into a trubrics friendly object, and must be initialised before using the [ModelValidator](#validate-a-model-with-the-modelvalidator) or the [FeedbackCollector](#collect-user-feedback-with-the-feedbackcollector). The `DataContext` requires a testing_data pandas dataframe, and the name of the target value column. Optionally, training_data may be specified, as in the following example:
```py
from trubrics.example import get_titanic_data_and_model
train_df, test_df, model = get_titanic_data_and_model()

from trubrics.context import DataContext
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to validate model on
    training_data=train_df,  # optional training data for certain validations
    target="Survived",
)
```

## Validate a model with the ModelValidator
The `ModelValidator` holds a number of out-of-the-box validations that can be directly applied to the `DataContext` and an ML model:
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
validations = [
    model_validator.validate_performance_against_threshold(
        metric="accuracy", threshold=0.7
    ),
    model_validator.validate_performance_between_train_and_test(
        metric="recall", threshold=0.3
    ),
]
```

The list of validations above can then be saved to a local .json file as a **trubric**:
```py
from trubrics.validations import Trubric
trubric = Trubric(
    name="my_first_trubric",
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,
)
trubric.save_local(path=".")
```
The trubric defines the gold standard of validations required for the project, and may be used to validate any combination of model and `DataContext`.

*See a full tutorial on the titanic dataset [here](https://trubrics.github.io/trubrics-sdk/notebooks/titanic-demo.html)*.

## Collect user feedback with the FeedbackCollector
Trubrics feedback components help you build python applications with your favourite library (e.g. [Streamlit](https://streamlit.io/)).
These are aimed at collecting feedback on your models from business users and translating these into validation points.

As with the ModelValidator, the `DataContext` is initialised and fed into the `FeedbackCollector`:
```python
import streamlit as st
from trubrics.example import get_titanic_data_and_model
from trubrics.context import DataContext
from trubrics.feedback import FeedbackCollector

train_df, test_df, model = get_titanic_data_and_model()
data_context = DataContext(
    testing_data=test_df,
    training_data=train_df,
    target="Survived",
    categorical_columns=["Sex", "Embarked", "Title"],  # for the FeedbackCollector, categorical columns must be specified in the DataContext
)

collector = FeedbackCollector(data=data_context, model=model)
```

The FeedbackController includes various methods to facilitate building an application with streamlit:

- **What-if experimentation**: generate a series of user inputs from the testing_data of the `DataContext`
    ```python
    with st.sidebar:
        st.title("Modify features to test the model...")
        collector.generate_what_if()
    ```

- **Feedback collection**: save various feedback types to a local .json file
    ```python
    st.title("View model prediction")
    st.text(collector.what_if_prediction)

    st.title("Send model feedback")
    collector.save_feedback(path=".", file_name="feedback.json")
    ```

*Run our demo user feedback app on the titanic dataset & model with the cli command:*
```console
(venv)$ trubrics example-titanic-app
```
![img](assets/titanic-feedback-example.png)

## Watch our "Getting Started" demo
[![img](./assets/trubrics-demo-youtube.png)](https://www.youtube.com/watch?v=I-lUGhHss5g)
