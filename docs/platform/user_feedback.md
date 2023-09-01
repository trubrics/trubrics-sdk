## Saving feedback to Trubrics
Upon creating a feedback component in [Trubrics](https://trubrics.streamlit.app/), a code snippet is generated for users to incorporate into their apps. There are several ways to save feedback:

### 1. With the Python SDK
Install Trubrics with:

```console
pip install trubrics
```

Set [Trubrics](https://trubrics.streamlit.app/) `email` and `password` as environment variables:

```bash
export TRUBRICS_EMAIL="trubrics_email"
export TRUBRICS_PASSWORD="trubrics_password"
```

and push some feedback to the `default` feedback component:

```python
import os
from trubrics import Trubrics

trubrics = Trubrics(
    project="default",
    email=os.environ["TRUBRICS_EMAIL"],
    password=os.environ["TRUBRICS_PASSWORD"],
)

user_feedback = trubrics.log_feedback(
    component="default",
    model="gpt-3.5-turbo",
    prompt_id=None,  # see `Prompts` to store user prompts and model generations
    user_response={
        "type": "thumbs",
        "score": "👎",
        "text": "Not a very funny joke...",
    }
)
```

!!!note "`trubrics.log_feedback()` arguments"
    :::trubrics.Trubrics.log_feedback

### 2. With Streamlit
Trubrics has an out-of-the-box [integration with Streamlit](../integrations/streamlit.md):

```console
pip install "trubrics[streamlit]"
```

```python
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector(
    project="default",
    email=st.secrets.TRUBRICS_EMAIL,
    password=st.secrets.TRUBRICS_PASSWORD,
)

collector.st_feedback(
    component="default",
    feedback_type="thumbs",
    open_feedback_label="[Optional] Provide additional feedback",
    model="gpt-3.5-turbo",
    prompt_id=None,  # see `Prompts` to log prompts and model generations
)
```

Take a look at our [demo LLM app](https://trubrics-llm-example-chatbot.streamlit.app/) for an example.

### 3. With Flask

[Here](../integrations/flask_example.md) is an example of how the python SDK can be used with a Flask app.

### 4. With React

[Here](../integrations/react_js.md) is an example showing how to collect feedback from a React app.

## Types of feedback
Each feedback response in a component must be of a particular type, as seen in the `user_response` field of the Feedback data object.

!!!note "Feedback object"
    <!-- :::trubrics.platform.feedback.Feedback -->

There are three out-of-the-box types of feedback:

- `thumbs` feedback (👍, 👎), with an optional open text box
- `faces` feedback (😞, 🙁, 😐, 🙂, 😀), with an optional open text box
- `textbox` feedback, an open text box for purely qualitative feedback

To save custom feedback with multiple fields, such as collecting survey responses, users can make use of the Feedback `metadata` field.

## Analyse quantitative user feedback in Trubrics

Various filters allow AI teams to:

- Aggregate responses by a frequency (hourly, daily, weekly, monthly)
- View all responses for a given score, model or user
- Compare responses for all scores, models or users

!!!tip
    All quantitative analysis is viewed per feedback component. Each feedback component should have a unique set of scores (i.e a unique [type](#types-of-feedback)) for analysis to be correctly computed.

## Review user comments

User comments are collected in the `text` field of `user_response`. All comments are listed in the `Comments` tab, and may be grouped together to create an [issue](issues.md).

## Export all raw data

Export a raw json file of all responses allows AI teams to conduct their own analysis. Use the \`📥 Download all\` button for a full export to json.
