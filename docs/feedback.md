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
from trubrics.cli.main import init
from trubrics.feedback.dataclass import Feedback

# init the trubrics platform connection with a project
init(project_name="<project_name>")

# save feedback
trubrics_feedback = Feedback(
    feedback_type="thumbs",
    user_response={"User satisfaction: thumbs": "👎"},
    data=None,
    model="model_reference",
    tags=["example"],
)
# set email and password to None to use your default connection from init
trubrics_feedback.save_ui(email=None, password=None)

# save feedback to a local .json file
trubrics_feedback.save_local("./example_feedback.json")
```
