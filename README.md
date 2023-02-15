# Welcome to the trubrics-sdk

---

<center>

![logo-gradient](./assets/logo-gradient.png)

[trubrics.com](https://www.trubrics.com/home)

_Investigate models, collaborate across teams, validate machine learning._

</center>

---

The trubrics-sdk is a python library for validating machine learning with data science and domain expertise. This is achieved by collecting business user feedback, creating ML validations with this feedback, and building repeatable validation checklists - a trubric.

## Key Features

- ML model validation with the [ModelValidator](#validate-a-model-with-the-modelvalidator)
- Feedback collection on ML models / data from users with the [FeedbackCollector](#collect-user-feedback-with-the-feedbackcollector)
- Tracking and management of validation runs and feedback in the [Trubrics platform](#track-all-validation-runs-and-feedback-in-trubrics)

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
2. Build validations with the `ModelValidator`, using the `DataContext` and any ML model (scikit-learn or [any python model](https://trubrics.github.io/trubrics-sdk/models/)). The `ModelValidator` holds a number of [out-of-the-box validations](https://trubrics.github.io/trubrics-sdk/validations/) and can also be used to build [custom validations](https://trubrics.github.io/trubrics-sdk/custom_validations/) from a python function.
3. Group validations into a `Trubric`, which is  saved as a .json file and rerun against any model / dataset.

Try out these steps by creating your own Trubric with this example:

```py
from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.validations import ModelValidator, Trubric

_, test_df, model = get_titanic_data_and_model()

# 1. Init DataContext
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to validate model on
    target="Survived",
)

# 2. Build validations with ModelValidator
model_validator = ModelValidator(data=data_context, model=model)
validations = [
    model_validator.validate_performance_against_threshold(metric="accuracy", threshold=0.7),
    model_validator.validate_feature_in_top_n_important_features(feature="Age", top_n_features=3),
]

# 3. Group validations into a Trubric
trubric = Trubric(
    name="my_first_trubric",
    data_context_name=data_context.name,
    data_context_version=data_context.version,
    validations=validations,
)
trubric.save_local()
```

The `Trubric` defines the gold standard of validations required for your project, and may be used to validate any combination of model and `DataContext`. Once saved as a .json, the trubric may be run directly from the [CLI](https://trubrics.github.io/trubrics-sdk/run_trubrics/).

_See a full tutorial on the titanic dataset [here](https://trubrics.github.io/trubrics-sdk/notebooks/titanic-full-demo.html)_.

## Collect user feedback with the FeedbackCollector

Trubrics feedback components help you collect feedback on your models with your favourite python web development library. Once feedback has been collected from business users, it should be translated into validation points to ensure repeatable validations  throughout the lifetime of the model. Add the trubrics feedback component to your ML apps now to start collecting feedback:

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
    path="./feedback_issue.json",  # path to save feedback .json
    tags=["streamlit"],
    metadata={"some": "metadata"},
    save_ui=False,  # set to True to save feedback to Trubrics
)
```

</td>
</tr>
</table>

<details>
  <summary>Dash and Gradio integrations</summary>

<table>
<tr>
<th> Framework </th>
<th style="text-align:center"> Getting Started Code Snippets </th>
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
        collect_feedback_dash()
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
    collect_feedback_gradio()

demo.launch()
```

</td>
</tr>
</table>
</details>

You can view our demo user feedback app, using the streamlit feedback collector and an example experimentation tool, on the titanic dataset & model on [Hugging Face Spaces](https://huggingface.co/spaces/trubrics/trubrics-titanic-demo), or run it locally with the CLI command:

```console
(venv)$ trubrics example-app
```

<p align="center"><img src="./assets/titanic-feedback-example.png"/></p>

## Track all validation runs and feedback in Trubrics

The Trubrics platform allows teams to collaborate on model issues and track validation changes. Please get in touch with us [here](https://trubrics.com/demo/) to gain access to Trubrics for you and your team.

[![img](assets/trubrics-login.png)](https://trubrics.com/demo/)

### `trubrics init` will initialise your terminal and authenticate with your Trubrics account

<p align="center"><img src="./assets/trubrics-init.gif"/></p>

### `trubrics run` will run your validations from the terminal and track them in Trubrics

<p align="center"><img src="./assets/trubrics-run.gif"/></p>

## Watch our getting started demo

[![img](assets/yt-gs.png)](https://www.youtube.com/watch?v=gMK2ut_I4a0)
