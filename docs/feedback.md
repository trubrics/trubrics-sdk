# Gather feedback from business users

Trubrics feedback components help you build python applications with your favourite library (e.g. [Streamlit](https://streamlit.io/)).
These are aimed at collecting feedback on your models from business users, for further translation into validation points.

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

The FeedbackCollector includes various methods to facilitate building an application with streamlit:

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