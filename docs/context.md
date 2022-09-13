# Understanding contexts in trubrics
Contexts in the trubrics library refer to [Pydantic](https://pydantic-docs.helpmanual.io/) data models. The DataContext must be configured before creating either a `ModelValidator` or a feedback component.

## The DataContext
!!!example "DataContext Example"
    --8<-- "docs/snippets/init_datacontext.md"
:::trubrics.context.DataContext

## The TrubricContext
!!!example "TrubricContext Example"
    --8<-- "docs/snippets/save_trubric.md"
:::trubrics.context.TrubricContext

???note "The ValidationContext"
    The ValidationContext is an intermediate context used to define the output of a trubrics validation.
    ValidationContexts are gathered into a list to define a trubric.

    :::trubrics.context.ValidationContext

## The FeedbackContext
:::trubrics.context.FeedbackContext
