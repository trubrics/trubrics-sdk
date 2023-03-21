# Welcome to the trubrics-sdk

---

<center>

![logo-gradient](./assets/logo-gradient.png)

[trubrics.com](https://www.trubrics.com/home)
</center>

---

The trubrics-sdk allows ML practitioners to collect human feedback on datasets & ML models, and integrate this feedback into the ML workflow.

## Key Features

- Feedback collection on ML models / data from users with the [FeedbackCollector](#collect-human-feedback-with-the-feedbackcollector)
- Integration of feedback into ML workflows with the [ModelValidator](#validate-a-model-with-the-modelvalidator)
- Tracking and management of user feedback in the [Trubrics platform](#track-all-feedback-and-validations-in-trubrics)

## Install (Python 3.7+)

```console
(venv)$ pip install trubrics
```

## Collect human feedback with the FeedbackCollector

The Trubrics FeedbackCollector helps you to collect user feedback on your models with your favourite python web development library. Exposing ML data and model results to users / domain experts is a great way to find bugs and issues. To close the loop on feedback issues and ensure they are not repeated, Data Scientists can build validations using the [ModelValidator](#validate-a-model-with-the-modelvalidator).

Start collecting feedback directly from within your ML apps now with our various integrations:

### Streamlit

👇 click here to view our demo app

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trubrics-titanic-example.streamlit.app)

<img src="./assets/streamlit-cloud-demo.png"  width="800">

To start collecting feedback from your [Streamlit](https://streamlit.io/) app, install the additional dependency:

```console
(venv)$ pip install "trubrics[streamlit]"
```

and add this code snippet directly to your streamlit app:
```py
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()
collector.st_feedback(type="issue")  # feedback is saved to a .json file
```

For more information on our Streamlit integration, check our [docs](https://trubrics.github.io/trubrics-sdk/feedback/).

<details>
  <summary>Dash</summary>

To get started with [Dash](https://dash.plotly.com/), install the additional dependency:

```console
(venv)$ pip install "trubrics[dash]"
```

And add this to your Dash app:
```py
from dash import Dash, html

from trubrics.integrations.dash import collect_feedback

app = Dash(__name__)

app.layout = html.Div([collect_feedback(tags=["Dash"])])

if __name__ == "__main__":
    app.run_server(debug=True)
```
</details>

<details>
  <summary>Gradio</summary>

To get started with [Gradio](https://gradio.app/), install the additional dependency:

```console
(venv)$ pip install "trubrics[gradio]"
```

And add this to your Gradio app:
```py
import gradio as gr

from trubrics.integrations.gradio import collect_feedback

with gr.Blocks() as demo:
    gr.Markdown("Gradio app to collect user feedback on models.")
    with gr.Tab("Feedback"):
        collect_feedback(tags=["Gradio"])

demo.launch()
```
</details>

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
trubric.save_local(path="./my_first_trubric.json")  # save trubric as a local .json file
trubric.save_ui()  # or to the Trubrics platform
```

The `Trubric` defines the gold standard of validations required for your project, and may be used to validate any combination of model and `DataContext`. Once saved as a .json, the trubric may be run directly from the [CLI](https://trubrics.github.io/trubrics-sdk/run_trubrics/).

_See a full tutorial on the titanic dataset [here](https://trubrics.github.io/trubrics-sdk/notebooks/titanic-full-demo.html)_.


## Track all feedback and validations in Trubrics

The Trubrics platform allows teams to collaborate on model issues and track validation changes. Please get in touch with us [here](https://trubrics.com/demo/) to gain access to Trubrics for you and your team.

[![img](assets/trubrics-login.png)](https://trubrics.com/demo/)

### `trubrics init` will initialise your terminal and authenticate with your Trubrics account

<p align="center"><img src="./assets/trubrics-init.gif"/></p>

### `trubrics run` will run your validations from the terminal and track them in Trubrics

<p align="center"><img src="./assets/trubrics-run.gif"/></p>

## Watch our getting started demo

[![img](assets/yt-gs.png)](https://www.youtube.com/watch?v=gMK2ut_I4a0)
