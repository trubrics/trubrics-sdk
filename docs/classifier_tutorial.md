# Titanic classifier example

In this tutorial we will train a classifier on the [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic) dataset. The goal is to show an end to end example of how you can develop validations for your model (both out of the box and custom), and get business user feedback on your model to incorporate into you validation workflow.

## 0 Clone the git repo
```console
$ git clone https://github.com/trubrics/trubrics-sdk.git
```

## 1 Train model
To train a titanic classifier and save locally, run:
```console
(venv)$ make train-titanic
```

## 2 Collect user feedback [optional]
Run the streamlit app to collect user feedback on your model
```console
(venv)$ make streamit-demo
```

## 3 Create a trubric of validation points
In `jupyter lab`, run the cells in the `examples/titanic-demo.ipynb`. The notebook can equally be seen in the [here](notebooks/titanic-demo.ipynb).
