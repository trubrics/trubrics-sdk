# Gather feedback from business users

The Trubrics FeedbackCollector helps you to collect user feedback on your models with your favourite python web development library. Exposing ML data and model results to users / domain experts is a great way to find bugs and issues. To close the loop on feedback issues and ensure they are not repeated, Data Scientists can build validations using the [ModelValidator](./validations.md).

!!!tip "Trubrics platform access"
    The Trubrics platform will allow you to track all issues, and discuss errors with users and other collaborators. There are also capabilities to close feedback issues by linking to specific validation runs. Creating accounts for users will also allow authentication directly in the FeedbackCollector. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access for you and your team.

## Integrations

See our integrations for various implementations of the FeedbackCollector:

- [Streamlit](./streamlit.md)
- [Gradio](./gradio.md)
- [Dash](./dash.md)

## Examples

See our python examples:

- [Flask example](./flask_example.md)

## Python SDK

To save feedback to the Trubrics platform:

```python
---8<-- "examples/feedback_apps/python_sdk.py"
```
