# Understanding contexts in trubrics
Contexts in the trubrics library refer to [Pydantic](https://pydantic-docs.helpmanual.io/) data models. The two main contexts that must be initialised before building a validations or a feedback component are the DataContext and the ModelContext.

<center>
```mermaid
graph LR
    subgraph init [Initialisation]
    D[DataContext]
    M[ModelContext]
    end
    subgraph val [Building DS validations]
    V([ValidationContext]) --> T[TrubricContext]
    end
    subgraph feed [Building feedback components]
    F[FeedbackContext]
    end
    D --> V
    M --> V
    D --> F
    M --> F
```
</center>

## The DataContext
!!!example "DataContext Example"
    --8<-- "docs/snippets/init_datacontext.md"

:::trubrics.context.DataContext

## The ModelContext
:::trubrics.context.ModelContext

## The TrubricsContext
:::trubrics.context.TrubricContext

???note "The ValidationContext"
    The ValidationContext is an intermediate context used to define the output of a trubrics validation.
    ValidationContexts are gathered into a list to define a trubric.

## The FeedbackContext
:::trubrics.context.FeedbackContext
