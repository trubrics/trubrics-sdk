
!!!warning "trubrics>1.4.2"
    Validations in Trubrics will soon be moved to another repository. For trubrics>1.4.2 users, please install all validations dependencies with:
    ```
    pip install "trubrics[validations]"
    ```

A number of different tutorials are available with examples of how to apply validations to [classification](#classification) or [regression](#regression) models:

## Classification

For classification models, we are using the [Titanic Use Case](https://www.kaggle.com/c/titanic):

1. **Full validations (out-of-the-box and custom) demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/main/examples/validations/classification_titanic/classification_full_demo.ipynb)
  
2. **Custom validations and custom model demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/main/examples/validations/classification_titanic/custom_validations/titanic_custom_validations.ipynb)

3. **Trubrics platform demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/main/examples/validations/classification_titanic/trubrics_platform_demo.ipynb)
   
## Regression

For regression models, we are using Kaggle's [house prices prediction](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) dataset. Clone the repo to run the notebook.

1. **Regression validations demo**: [.ipynb](https://github.com/trubrics/trubrics-sdk/blob/main/examples/validations/regression_house_prices/house_prices_demo.ipynb)


## MLflow

Clone the repo to run the notebook. Read more about our MLflow plugin [here](../integrations/mlflow.md).

1. **Validate data or models within MLflow**: [.ipynb](https://github.com/trubrics/trubrics-sdk/blob/main/examples/validations/mlflow/mlflow-trubrics.ipynb)
