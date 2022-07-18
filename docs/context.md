# Understanding contexts in trubrics
Contexts in the trubrics library refer to [Pydantic](https://pydantic-docs.helpmanual.io/) data models. The two main contexts that must be initialised before building a trubric or a feedback component are the DataContext and the ModelContext.

<center>
``` mermaid
classDiagram
  TrubricsContext <|-- DataContext
  TrubricsContext <|-- ModelContext
  FeedbackContext <|-- DataContext
  FeedbackContext <|-- ModelContext
```
</center>

## The DataContext
:::trubrics.context.DataContext

## The ModelContext


## The ValidationContext


## The TrubricsContext


## The FeedbackContext
