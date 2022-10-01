# The DataContext
Contexts in the trubrics library refer to [Pydantic](https://pydantic-docs.helpmanual.io/) data models. The DataContext must be configured before creating either a `ModelValidator` or a `FeedbackCollector`.

## The DataContext
!!!example "DataContext Example"
    --8<-- "docs/snippets/init_datacontext.md"
:::trubrics.context.DataContext
