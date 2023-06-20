# Collect user feedback

The main purpose of the trubrics-sdk is to provide AI practitioners with UI widgets and an API to save user feedback to [Trubrics](https://trubrics.streamlit.app/). All feedback is organised into feedback components, each of which have their own type.


!!!note "Feedback object"
    :::trubrics.feedback.dataclass.Feedback


## Types of feedback
There are three out-of-the-box types of feedback:

- `thumbs` feedback (👍, 👎), with an optional open text box
- `faces` feedback (😞, 🙁, 😐, 🙂, 😀), with an optional open text box
- `textbox` feedback, an open text for purely qualitative feedback

To save custom feedback with multiple fields, such as collecting survey responses, users can use Feedback `metadata`.

## Create a feedback component

!!!tip
    Trubrics currently supports user feedback collection from python environments. [Contact us](https://trubrics.com/contact-us/) to discuss all other options.

- Push feedback instantly to the `default` feedback component
    - with the [LLM demo](https://trubrics-llm-example.streamlit.app/)
    - with python / streamlit
- Create a feedback component
- Analyse quantitative user feedback
- Review user comments
- Create AI issues from user comments

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
