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
- Collect feedback from business users on models with python web development components with [Streamlit](https://streamlit.io/), [Dash](https://dash.plotly.com/) or [Gradio](https://gradio.app/).
- Out of the box & custom validations (python functions) to build around models & datasets with the **trubrics ModelValidator** (currently supporting tabular data).
- **Trubrics CLI** tool to run a list of saved validations (a **trubric**) against new models or datasets in a CI/CD/CT pipeline.
<center>

![](./assets/trubrics-explain-dark.png#gh-dark-mode-only)
![](./assets/trubrics-explain-light.png#gh-light-mode-only)
</center>

## Install (Python 3.7+)
```console
(venv)$ pip install trubrics
```

## Validate a model with the ModelValidator
There are three basic steps to creating model validations with the trubrics-sdk:

1. Initialise a `DataContext`, that wraps ML datasets and metadata into a trubrics friendly object.
2. Feed the `DataContext` and an ML model (scikit-learn or [any other model](https://trubrics.github.io/trubrics-sdk/models/)) into the `ModelValidator`, that holds a number of [out-of-the-box validations](https://trubrics.github.io/trubrics-sdk/validations/) and can also be used to build [custom validations](https://trubrics.github.io/trubrics-sdk/custom_validations/).
3. Group the list of validations created into a `Trubric`, that can then be saved to a local .json file.

Try out these steps by creating your own Trubric with this example:
```py
from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.validations import ModelValidator, Trubric

_, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to validate model on
    target="Survived",
)

model_validator = ModelValidator(data=data_context, model=model)
validations = [
    model_validator.validate_performance_against_threshold(metric="accuracy", threshold=0.7),
    model_validator.validate_feature_in_top_n_important_features(feature="Age", top_n_features=3),
]
trubric = Trubric(
    name="my_first_trubric",
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,
)
trubric.save_local(path=".")
```

The trubric defines the gold standard of validations required for the project, and may be used to validate any combination of model and `DataContext`. Once saved as a .json, the trubric may be run directly with a [CLI](https://trubrics.github.io/trubrics-sdk/run_trubrics/).

*See a full tutorial on the titanic dataset [here](https://trubrics.github.io/trubrics-sdk/notebooks/titanic-demo.html)*.

## Collect user feedback with the FeedbackCollector
Trubrics feedback components help you to collect feedback on your models with your favourite python library. Once feedback has been collected from business users, it should be translated into validation points to ensure repeatable checking throughout the lifetime of the model. Add the trubrics feedback component to your ML apps now to start collecting feedback:

<table>
<tr>
<th> Framework </th>
<th style="text-align:center"> Getting Started Code Snippets </th>
</tr>
<tr>
<td>

[Streamlit](https://streamlit.io/)

</td>
<td>

```py
from trubrics.feedback import collect_feedback_streamlit

collect_feedback_streamlit(
    path=".",  # path to feedback .json file
    file_name=None,  # file name, if None defaults to feedback.json
    metadata=None,  # a dict of any metadata to save from you app
    tags=None  # a list of any tags for this feedback file
)
```

</td>
</tr>
<tr>
<td>

[Dash](https://dash.plotly.com/)

</td>

<td>

```py
from dash import Dash, html

from trubrics.feedback import collect_feedback_dash

app = Dash(__name__)

app.layout = html.Div(
    [
        collect_feedback_dash(
            path=".",  # path to feedback .json file
            file_name=None,  # file name, if None defaults to feedback.json
            metadata=None,  # a dict of any metadata to save from you app
            tags=None  # a list of any tags for this feedback file
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

</td>
</tr>
<tr>
<td>

[Gradio](https://gradio.app/)

</td>
<td>

```py
import gradio as gr

from trubrics.feedback import collect_feedback_gradio

with gr.Blocks() as demo:
    collect_feedback_gradio(
        path=".",  # path to feedback .json file
        file_name=None,  # file name, if None defaults to feedback.json
        metadata=None,  # a dict of any metadata to save from you app
        tags=None  # a list of any tags for this feedback file
    )

demo.launch()
```

</td>
</tr>
</table>

You can view our demo user feedback app, using the streamlit feedback collector and an example experimentation tool, on the titanic dataset & model on [Hugging Face Spaces](https://huggingface.co/spaces/trubrics/trubrics-titanic-demo), or run it locally with the CLI command:
```console
(venv)$ trubrics example-app
```
![img](assets/titanic-feedback-example.png)

## Watch our getting started demo
[![img](assets/yt-gs.png)](https://www.youtube.com/watch?v=gMK2ut_I4a0)
