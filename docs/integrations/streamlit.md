# FeedbackCollector Streamlit Integration
The FeedbackCollector takes user feedback from within an app and saves it to Trubrics.

## Install
To get started with [Streamlit](https://streamlit.io/), install the additional dependency:

```console
pip install "trubrics[streamlit]"
```

## Streamlit Example Apps
Once you have created an account with [Trubrics](https://trubrics.streamlit.app/), you can try two deployed example Streamlit apps that use the integration to save feedback:

- [LLM](https://trubrics-llm-example.streamlit.app/): An LLM app that queries OpenAI's API and allows users to leave feedback on text generations.
- [Titanic](https://trubrics-titanic-example.streamlit.app/): An app that allows users to give feedback on a classifier that predicts whether passengers will survive the titanic.

The code for these apps can be viewed in the [trubrics-sdk](https://github.com/trubrics/trubrics-sdk/tree/main/examples), and may be run by cloning the repo and running:

=== "LLM"

    ```console
    streamlit run examples/feedback/llm/llm_streamlit_app.py
    ```

=== "Titanic"

    ```console
    streamlit run examples/feedback/titanic/titanic_streamlit_app.py
    ```

## Add the FeedbackCollector to your App
To get started with the bare bones code, you can add this code snippet directly to your streamlit app:
```py
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector

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

What's going on here? Let's break down this snippet:

1. The [FeedbackCollector](#feedbackcollector) holds Trubrics account information

    !!!tip "FeedbackCollector object"
        :::trubrics.integrations.streamlit.FeedbackCollector.__init__

2. Its [st_feeedback()](#st_feedback) method allows users to embed UI widgets in their apps

    !!!tip ".st_feedback() parameters"
        :::trubrics.integrations.streamlit.FeedbackCollector.st_feedback

!!!Note
    Each feedback component holds a unique type of feedback. You should create multiple `FeedbackCollector` for collecting different types of feedback in the same app.

## Trubrics UI components
All of the UI components that you can see here are also available as standalone visual components without the saving functionality. For example, generate the faces UI component with:

```py
output = collector.st_faces_ui(disable_on_click=True)
st.write(output)
```

The `disable_on_click=True` parameter disables other buttons that are not clicked. Users can re-click the button to reverse this behaviour.
