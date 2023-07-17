# Compatible models with the ModelValidator

!!!warning "trubrics>1.4.2"
    Validations in Trubrics will soon be moved to another repository. For trubrics>1.4.2 users, please install all validations dependencies with:
    ```
    pip install "trubrics[validations]"
    ```

## 1. Load a scikit-learn model
Trubrics integrates natively with the [scikit-learn API](https://scikit-learn.org/stable/modules/classes.html), meaning any sklearn model may be inserted directly into a `ModelValidator` to create validations. This also means that we encourage you to use scikit's [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline) object to include all model processing transformations in a single object.

## 2. Load your own model
:::tests.test_validations.test_custom_model.RuleBasedModel
    options:
        show_root_toc_entry: false
        members:
            -
