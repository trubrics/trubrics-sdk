# Welcome to the trubrics-sdk
-------

<center>

![logo-gradient](./assets/logo-gradient.png)

[trubrics.com](https://www.trubrics.com/home)

*Investigate models, collaborate across teams, validate machine learning.*
</center>

-------

Trubrics grows confidence and trust in machine learning by bridging the gap between data scientists and business users. The trubrics-sdk is a python library to validate machine learning with data science and domain expertise. This is achieved by collecting business user feedback, combining feedback with data science knowledge to create actionable validation points, and building repeatable validation checklists - a trubric.
<br>
<br>
<center>

![trubrics-explain](./assets/trubrics-explain.png)
</center>

## Key Features
- Out of the box validations to build around models & datasets (currently supporting tabular data)
- Custom validations as python functions to validate your models
- A CLI tool to run saved validations against new models in a CI/CD/CT pipeline
- Python web development components (e.g. with [Streamlit](https://streamlit.io/)) to gather feedback from business users on models

## Install (Python 3.7+)
```console
(venv)$ pip install trubrics
```

## Create a trubric
A trubric is a checklist of validations, and can be built by:

1. Initialising `DataContext` object to wrap ML datasets into a trubrics friendly format
```py
from trubrics.context import DataContext
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to test against a model
    target="target_column_name_in_test_df"
)
```

2. Using the `ModelValidator` object to generate out of the box validations
```py
from trubrics.validations import ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
validations = [
    model_validator.validate_performance_against_threshold(
        metric="precision", threshold=0.8
    ),
    model_validator.validate_performance_against_threshold(
        metric="recall", threshold=0.7
    )
]
```

3. Saving a .json of all validations locally using a `Trubric` object
```py
from trubrics.validations import Trubric
trubric = Trubric(
    name="my_first_trubric",
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,
)
trubric.save_local(path="/local_data_folder")
```

*See a full tutorial on the titanic dataset [here](https://trubrics.github.io/trubrics-sdk/notebooks/titanic-demo.html)*.

## Collect model feedback
Trubrics feedback components help you build python applications with your favourite library (e.g. [Streamlit](https://streamlit.io/)).
These are aimed at collecting feedback on your models from business users and translating these into validation points.
Build a feedback application by:

1. As with [Create a Trubric](#create-a-trubric), initialise a `DataContext` to wrap your ML datasets into a trubrics friendly object
```py
from trubrics.context import DataContext
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to test against a model
    target="target_column_name_in_test_df"
)
```

2. Using the `StreamlitComponent` object to generate app components to collect feedback
```python
import streamlit as st
from trubrics.feedback_components.streamlit import StreamlitComponent

st_component = StreamlitComponent(model=model, data=data_context)

with st.sidebar:
    st.title("Modify features to test the model...")
    what_if_df = st_component.generate_what_if(TESTING_DATA)

st.title("View model prediction")
raw_prediction = st_component.model.estimator.predict(what_if_df)[0]  # type: ignore
if raw_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
st_component.feedback(what_if_df=what_if_df, model_prediction=raw_prediction, tracking=True)
```

## Watch our "Getting Started" demo
[![img](./assets/trubrics-demo-youtube.png)](https://www.youtube.com/watch?v=I-lUGhHss5g)
