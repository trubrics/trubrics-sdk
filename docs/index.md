# Welcome to the trubrics-sdk
For the trubrics website visit [trubrics.com](https://www.trubrics.com/home).

-------
<center>
![logo-gradient](./assets/logo-gradient.png)
*Combine data science knowledge with business user feedback to validate machine learning.*
</center>

-------

Trubrics bridges the gap between data science understanding of business challenges, and business understanding of data science outputs. The trubrics-sdk is a python library to collect business user feedback for machine learning, combine feedback with data science knowledge into actionable validation points, and build repeatable validation checklists - a trubric.

<center>
![trubrics-explain](./assets/trubrics-explain.png)
</center>

## Key Features
- [Out of the box validations](validations.md) to build around models & datasets (currently supporting tabular data)
- An object to write [custom validations](custom_validations.md)
- [A CLI tool](run_trubrics.md) to execute validations against new models in a CI/CD/CT pipeline
- Python web development components (e.g. with streamlit) to [gather feedback from business users](feedback.md) on models
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

:::examples.trubrics_config

## Build a python app to collect model feedback
Trubrics components can be built with your favourite python web development framework:

1. Initialising `DataContext` and `ModelContext` objects to wrap your data and models into a trubrics friendly format
--8<-- "docs/snippets/init_datacontext.md"
--8<-- "docs/snippets/init_modelcontext.md"
2. Using the `StreamlitComponent` object to generate app components to collect feedback
--8<-- "docs/snippets/streamlit_feedback.md"
