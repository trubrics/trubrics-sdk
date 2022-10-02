# The `ModelValidator` object

The trubrics library comes with [out-of-the-box validations](validations.md) that you can test against your models in a
couple of lines of code. These validations are held in the `ModelValidator` object, that can be instantiated
with a [DataContext](data_context.md) and a [model](models.md). This object can also be used to build [custom validations](custom_validations.md).

!!!example
    ```py
    
    ```

## Metrics & scoring functions
Many validations in the `ModelValidator` require the computation of a metric to validate. It is good practice to recompute these metrics outside of your training pipeline to avoid errors in passing on pre-computed metrics. Trubrics makes use of sklearn's 
