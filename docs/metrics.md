# Metrics and scoring functions
Many validations in the `ModelValidator` require the computation of a metric to validate. It is good practice to recompute these metrics outside of your training pipeline to avoid errors in passing on pre-computed metrics. 

## 1. Scikit-learn scoring functions
The `ModelValidator` makes use of [sklearn.metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics) to compute model performance on a given dataset in the [DataContext](data_context.md).

## 2. Custom scoring functions

## 3. Data Slicing functions
