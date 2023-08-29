# Welcome to the trubrics-sdk

Trubrics enables AI teams to **collect, analyse and manage user feedback** on their models.

<img src="./assets/trubrics-example.png"  width="800">

## Try our LLM demo

1. Create your **free account**:

    [<img src="./assets/sign_up.png"  width="200">](https://trubrics.streamlit.app/)

2. Save feedback to Trubrics from our **demo LLM app**:

    [<img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"  width="200">](https://trubrics-llm-example-chatbot.streamlit.app/)

Or watch a step by step video of integrating Trubrics into the LLM Streamlit app [here](https://www.youtube.com/watch?v=2Qt54qGwIdQ).

## Collect user feedback with the Python SDK

The python SDK allows you to collect user feedback from your ML apps from any python backend or web framework. Install it with:

```console
pip install trubrics
```

Now set your [Trubrics](https://trubrics.streamlit.app/) `email` and `password` as environment variables:

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

user_prompt = trubrics.log_prompt(
    model_config={"model": "gpt-3.5-turbo"},
    prompt="Tell me a joke",
    generation="Why did the chicken cross the road? To get to the other side.",
)

user_feedback = trubrics.log_feedback(
    component="default",
    model=user_prompt.model_config.model,
    prompt_id=user_prompt.id,
    user_response={
        "type": "thumbs",
        "score": "👎",
        "text": "Not a very funny joke...",
    }
)
```

## Collect user feedback from a Streamlit app

To start collecting feedback from your [Streamlit](https://streamlit.io/) app, install the additional dependency:

```console
pip install "trubrics[streamlit]"
```

and add this code snippet directly to your streamlit app:

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
    prompt_id=None,  # see log_prompt to log user prompts from Streamlit
)
```

## Collect user feedback from a React.js app

We have developed an [example](https://github.com/trubrics/trubrics-sdk/blob/main/examples/feedback/react_js) showing how you can collect feedback from a React app.

## Why should you monitor usage of your models?

- **🚨 Identify bugs** - users are constantly running inference on your models, and may be more likely to find bugs than your ML monitoring system
- **🧑‍💻️ Fine tune** - users often hold domain knowledge that can be useful to fine tune models
- **👥 Align** - identifying user preferences will help you to align models to your users

## What's next?

- If you haven't already, create a free account or sign in to [Trubrics](https://trubrics.streamlit.app/).
- Get more technical information from our [docs](trubrics.github.io/trubrics-sdk/):
    - **Collect** user feedback with ✏️ [Feedback components](https://trubrics.github.io/trubrics-sdk/platform/feedback_components/)
    - **Analyse** user feedback with 🪄 [Insights](https://trubrics.github.io/trubrics-sdk/platform/insights/)
    - **Manage** user feedback with ⚠️ [Issues](https://trubrics.github.io/trubrics-sdk/platform/issues/)
- Check out our [website](https://www.trubrics.com/home) for more information about Trubrics.
