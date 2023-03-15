# FeedbackCollector Streamlit Integration


## Install integration
To get started with [Streamlit](https://streamlit.io/), install the additional dependency:

```console
(venv)$ pip install "trubrics[streamlit]"
```

## Launch demo application from CLI

- Run our demo Streamlit app without authentication:
    ```console
    (venv)$ trubrics example-app
    ```
  
- Run our demo Streamlit app with authentication to the Trubrics platform:
    ```console
    (venv)$ trubrics example-app --trubrics-platform-auth multiple_users
    ```

    !!!tip "Trubrics platform access"
        The Trubrics platform will allow you to track all issues, and discuss errors with users and other collaborators. There are also capabilities to close feedback issues by linking to specific validation runs. Creating accounts for users will also allow authentication directly in the FeedbackCollector. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access for you and your team.

    ![logo-gradient](./assets/titanic-feedback-example.png)
    <p align="center"><em>Our demo Streamlit app with authentication to the Trubrics platform</em></p>


## Add the FeedbackCollector to your App

To get started with the bare bones code, you can add this code snippet to your app:
```py
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()
collector.st_feedback(type="issue")
```

We can breakdown this snippet in to:

1. The [FeedbackCollector](#feedbackcollector) object that holds metadata (about datasets, models and authentication)
2. Its [st_feeedback()](#st_feedback) method that allows users to collect different types of feedback
3. Its [st_trubrics_auth()](#st_trubrics_auth) method that allows users to authentication with the Trubrics platform

### FeedbackCollector()

!!!tip "Trubric object"
    :::trubrics.feedback.dataclass.Feedback

### .st_feedback()

### .st_trubrics_auth()
