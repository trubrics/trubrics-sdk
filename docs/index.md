# Welcome to the trubrics-sdk
For the trubrics website visit [trubrics.com](https://www.trubrics.com/home).

-------
<center>
![logo-gradient](./assets/logo-gradient.png)
*Combine data science knowledge with business user feedback to validate machine learning.*
</center>

-------

???note "Abstract"
    A lack of communication between data teams and the end business users result in Data Scientists not truly understanding the business problem they are solving and business users not understanding the machine learning model being delivered. Trubrics provides solutions to collect business user feedback for machine learning, combine feedback with data science knowledge into actionable validation points, and build repeatable validation checklists - a trubric.

## Install
--8<-- "docs/snippets/install.md"

## Create a trubric
Build validations by:

1. Initialising `DataContext` and `ModelContext` objects to wrap your data and models into a trubrics friendly format
--8<-- "docs/snippets/init_datacontext.md"
--8<-- "docs/snippets/init_modelcontext.md"
2. Using the `Validator` object to generate out of the box validations
--8<-- "docs/snippets/create_validations.md"
3. Saving a .json of all validations locally using a `TrubricsContext` object
--8<-- "docs/snippets/save_trubric.md"

## Run a trubric from the command line
To run a trubric in a CI/CD pipeline or in a continuous training pipeline for auto-validation of your model:
--8<-- "docs/snippets/trubrics_cli.md"
:::examples.trubrics_config

## Build a python app to collect model feedback
Trubrics components can be built with your favourite python web development framework:

1. Initialising `DataContext` and `ModelContext` objects to wrap your data and models into a trubrics friendly format
--8<-- "docs/snippets/init_datacontext.md"
--8<-- "docs/snippets/init_modelcontext.md"
2. Using the `StreamlitComponent` object to generate app components to collect feedback
--8<-- "docs/snippets/streamlit_feedback.md"
