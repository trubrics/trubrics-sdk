# Titanic classifier

In this tutorial we will train a classifier on the [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic) dataset. The goal is to show an end to end example of how you can develop validations for your model (both out of the box and custom), and get business user feedback on your model to incorporate into you validation workflow.

## 1 Train model
To train a titanic classifier and save locally, run:
```console
(venv)$ make train-titanic
```

## 2 Create a trubric of validation points
In `jupyter lab`, run the cells in the `titanic-demo.ipynb`.

## 3 Collect user feedback
Finally, run the streamlit app to collect user feedback on your model
```console
(venv)$ make streamit-demo
```
