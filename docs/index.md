# Welcome to the trubrics-sdk
For the trubrics website visit [trubrics.com](https://www.trubrics.com/home).

-------
<center>
![logo-gradient](./assets/logo-gradient.png)
*Combine data science knowledge with business user feedback to validate machine learning.*
</center>

-------

Trubrics bridges the gap between data scientists understanding of business challenges, and business users understanding of data science outputs. The trubrics-sdk is a python library to collect business user feedback for machine learning, combine feedback with data science knowledge into actionable validation points, and build repeatable validation checklists - a trubric.

<center>
![trubrics-explain](./assets/trubrics-explain.png)
</center>

## Key Features
- [Out of the box validations](validations.md) to build around models & datasets (currently supporting tabular data)
- An object to write [custom validations](custom_validations.md)
- [A CLI tool](run_trubrics.md) to run validations against new models in a CI/CD/CT pipeline
- Python web development components (e.g. with [Streamlit](https://streamlit.io/)) to [gather feedback from business users](feedback.md) on models
- A UI to track validation checklists per project - [coming soon](log_trubrics.md)

## Install (Python 3.7+)
--8<-- "docs/snippets/install.md"

## Create a trubric
A trubric is a checklist of validations, and can be built by:

1. Initialising `DataContext` and `ModelContext` objects to wrap data and models into a trubrics friendly format
--8<-- "docs/snippets/init_datacontext.md"
--8<-- "docs/snippets/init_modelcontext.md"
2. Using the `Validator` object to generate out of the box validations
--8<-- "docs/snippets/create_validations.md"
3. Saving a .json of all validations locally using a `TrubricsContext` object
--8<-- "docs/snippets/save_trubric.md"

## Run a trubric
Run the locally saved trubric .json with:
--8<-- "docs/snippets/trubrics_cli.md"

`<trubrics_config_file>.py` is a trubrics config file where you can initialise a `DataContext` and `ModelContext`.
The file must contain a variable RUN_CONTEXT, an instance of the TrubricRun class. For more information, visit the
[Running trubrics](run_trubrics.md) page.

???note "Example of `<trubrics_config_file>.py` from examples/trubrics_config.py"
    ```py
    --8<-- "examples/trubrics_config.py"
    ```


## Collect model feedback
Trubrics feedback components help you build python applications with your favourite library (e.g. [Streamlit](https://streamlit.io/)).
These are aimed at collecting feedback on your models from business users and translating these into validation points.
Build a feedback application by:

1. Initialising `DataContext` and `ModelContext` objects to wrap your data and models into a trubrics friendly format
--8<-- "docs/snippets/init_datacontext.md"
--8<-- "docs/snippets/init_modelcontext.md"
2. Using the `StreamlitComponent` object to generate app components to collect feedback
--8<-- "docs/snippets/streamlit_feedback.md"
