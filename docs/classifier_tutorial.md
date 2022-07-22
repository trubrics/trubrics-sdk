# Titanic classifier example

In this tutorial we will train a classifier on the [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic) dataset. The goal is to show an end to end example of how you can develop validations for your model (both out of the box and custom), and get business user feedback on your model to incorporate into your validation workflow.

## 1 Clone the git repo
```console
$ git clone https://github.com/trubrics/trubrics-sdk.git
```

## 2 Train model
To train a titanic classifier and save a model locally, run:
```console
(venv)$ make train-titanic
```

## 3 Collect user feedback [optional]
Run the streamlit app to collect user feedback on your model
```console
(venv)$ make streamit-demo
```

## 4 Create a trubric of validation points
Follow along in `jupyter lab` by running the cells in the `examples/titanic-demo.ipynb`, or take a look at the notebook [here](notebooks/titanic-demo.html).
