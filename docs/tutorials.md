A number of different tutorials are available with examples of how to apply validations to [classification](#classification) or [regression](#regression) models:

## Classification

For classification models we are using the [Titanic Use Case](https://www.kaggle.com/c/titanic):

1. **Full validations demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/mrs_demo/examples/classification_titanic/classification_full_demo.ipynb)

      - Initialise a `DataContext` with ML datasets and metadata from the titanic use case
      - Build some out-of-the-box validations on a trained model and the `DataContext` with the `ModelValidator`:
          - Performance validations:
              - With sklearn metrics
              - With custom metrics
              - On specific data sclices
          - Explainability validations (with permutation importance)
          - Minimum functionality validation
          - Inference time validation
      - Build a custom **data validation**
      - Save validations to a `Trubric`
      - Execute the `Trubric` from file
      - Execute the `Trubric` from the CLI tool
  
2. **Custom validations demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/main/examples/classification_titanic/custom_validations/titanic-custom-validations.ipynb#scrollTo=b1f5da53-431b-4b76-8beb-be24bbfcef6b)

3. **Trubrics platform demo**: [![](./assets/colab-logo.png).ipynb](https://colab.research.google.com/github/trubrics/trubrics-sdk/blob/mrs_demo/examples/classification_titanic/trubrics_platform_demo.ipynb)
   
## Regression