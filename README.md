# Welcome to the trubrics-sdk

Trubrics enables AI teams to collect, analyse and manage user feedback on their models.

<img src="./assets/trubrics-example.png"  width="800">

## Install (Python 3.7+)

```console
(venv)$ pip install trubrics
```

## Create an account for free

Navigate to [**Trubrics**](https://trubrics.streamlit.app/) to create an account and start collecting user feedback from your AI applications:

```python
import os
import trubrics

config = trubrics.init(
    email=os.environ["TRUBRICS_EMAIL"],
    password=os.environ["TRUBRICS_PASSWORD"]
)

feedback = trubrics.Feedback(
    component_name="default",
    model="default_model",
    response={
        "type": "thumbs",
        "score": "👎",
        "text": "A comment / textual feedback from the user."
    },
)

trubrics.save(config, feedback)
```

## Streamlit integration

👇 **click here** to view our demo app with interactive examples and code snippets

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trubrics-titanic-example.streamlit.app)

To start collecting feedback from your [Streamlit](https://streamlit.io/) app, install the additional dependency:

```console
(venv)$ pip install "trubrics[streamlit]"
```

and add this code snippet directly to your streamlit app:
```python
import streamlit as st
from trubrics import FeedbackCollector

collector = FeedbackCollector(
    component_name="default",
    email=st.secrets["TRUBRICS_EMAIL"], # Store your Trubrics credentials in st.secrets:
    password=st.secrets["TRUBRICS_PASSWORD"], # https://blog.streamlit.io/secrets-in-sharing-apps/
)

collector.st_feedback(
    feedback_type="thumbs",
    model="your_model_name",
    open_feedback_label="[Optional] Provide additional feedback",
)
```

See our [docs](trubrics.github.io/trubrics-sdk/) or [website](https://www.trubrics.com/home) for more information.
