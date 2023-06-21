# FeedbackCollector Streamlit Integration
The FeedbackCollector takes user feedback from within an app and saves it as a local .json file, or directly to the Trubrics platform.

👇 **click here** to view our demo app with interactive examples and code snippets

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trubrics-titanic-example.streamlit.app)

## 1. Install the Streamlit integration
To get started with [Streamlit](https://streamlit.io/), install the additional dependency:

```console
(venv)$ pip install "trubrics[streamlit]"
```

## 2. Launch our demo application from the CLI
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


## 3. Add the FeedbackCollector to your App
To get started with the bare bones code, you can add this code snippet directly to your streamlit app:
```py
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()
collector.st_feedback(feedback_type="issue")
```

What's going on here? Let's break down this snippet:

1. The [FeedbackCollector](#feedbackcollector) object holds all metadata (about datasets, models and authentication)
2. Its [st_feeedback()](#st_feedback) method allows users to embed components in their apps to collect different
   types of feedback

!!!Note
    A second method [st_trubrics_auth()](#st_trubrics_auth) also exists, allowing users to authenticate with the Trubrics platform.

### FeedbackCollector()

All static metadata for the app that is not dependant on the actual feedback component can be included in the FeedbackCollector upon initialisation. This allows you to track what model was deployed (optional) and what datasets the user is viewing in your ML apps:

```py
from trubrics.example import get_titanic_data_and_model
from trubrics.integrations.streamlit import FeedbackCollector

# reading in some data and an ML model
_, test_df, model = get_titanic_data_and_model()


collector = FeedbackCollector(
    data="<link to cloud storage dataset>",
    model="<link to cloud storage model>",
)
```

!!!tip "FeedbackCollector object"
    :::trubrics.integrations.streamlit.FeedbackCollector.__init__

!!!Note
    For more information on authentication options and the `trubrics_platform_auth` attribute, see [st_trubrics_auth()](#st_trubrics_auth).

### .st_feedback()
Once the FeedbackCollector created, the .st_feedback() method is used to actually add visual feedback components to your app and to transform these inputs into [data](#feedback-data):

```py
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()
feedback = collector.st_feedback(feedback_type="faces")

feedback.dict() if feedback else None
```

The `st.feedback()` method returns a [pydantic](https://docs.pydantic.dev/) data object. Call `.dict()` on this variable to view the feedback in the app.

!!!tip ".st_feedback() parameters"
    :::trubrics.integrations.streamlit.FeedbackCollector.st_feedback

#### Feedback types
- `feedback_type="issue"`:
  The `issue` feedback_type provides a form with a title and description box for users to enter qualitative feedback.

  ![](./assets/feedback-issue.png){: style="width:70%"}

- `feedback_type="faces"`:
  The `faces` feedback_type provides a choice of 5 emoji faces. Add the parameter `open_feedback_label="An open text field"` to add an open text box for the user to optionally explain their choice.

  ![](./assets/feedback-faces.png){: style="width:50%"}

- `feedback_type="thumbs"`:
  The `thumbs` feedback_type provides a choice of 2 emoji thumbs. Add the parameter `open_feedback_label="An open text field"` to add an open text box for the user to optionally explain their choice.

  ![](./assets/feedback-thumbs.png){: style="width:20%"}

- `feedback_type="custom"`:
  The `custom` feedback_type allows developers to create any custom Streamlit code (e.g in an st.form() / a survey like style of open ended questions) and save it to a `Feedback` object with the `user_response={}` parameter.
  Here's an example:
  ```py
  from trubrics.integrations.streamlit import FeedbackCollector
  import streamlit as st

  collector = FeedbackCollector()

  custom_question = "Custom feedback slider"
  slider = st.slider(custom_question, max_value=10, value=5)
  submit = st.button("Save feedback")

  if submit and slider:
      collector.st_feedback(
          "custom",
          user_response={custom_question: slider},
      )
  ```
  ![](./assets/feedback-custom.png){: style="width:80%"}

#### Metadata
You can use the metadata argument to track specific data within your app, for example to be able to recreate the figure that your users are viewing:

```py
# save metadata of a specific component
st.pyplot(test_df["Age"].hist(figsize=(20, 10)).figure)
collector.st_feedback(feedback_type="issue", metadata={"age": test_df["Age"].to_list()})
```

![](./assets/feedback-metadata.png){: style="width:70%"}

#### Feedback data
Using `.st_feedback(path="./your_path/filename.json")` you can configure the path for each feedback to be saved to. The .json holds the following fields:

!!!tip "Feedback data object"
    :::trubrics.feedback.dataclass.Feedback

#### Trubrics UI components
All of the UI components that you can see here are also available as standalone visual components without the saving functionality. This allows you to use them as part of a custom feedback type:

```py
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()

output = collector.st_faces_ui(disable_on_click=True)

output
st.session_state
```

The `disable_on_click=True` parameter disables other buttons that are not clicked. Users can re-click the button to reverse this behaviour.

### .st_trubrics_auth()
To authenticate with the Trubrics platform, you must first run a [`trubrics init`](./validations/trubrics_cli.md#2-connect-to-the-trubrics-platform-with-trubrics-init) before launching your app.

You then have two options for saving feedback:

  1. `trubrics_platform_auth="single_user"`
     
    This allows users to add their feedback, but using the app owners credentials (that have been set with a `trubrics init`). Should you want to pass user information, you can always use the [`metadata`](#metadata) parameter of .st_feedback().

  2. `trubrics_platform_auth="multiple_users"`
     
    With this you can add full user authentication to within your streamlit application. Any user who has access to the Trubrics platform therefore can equally use their login details to login and start giving feedback.

    Here's an example of how you can add full user authentication to your app:

    ```py
    import streamlit as st
    from trubrics.integrations.streamlit import FeedbackCollector

    @st.cache_resource
    def trubrics_init():
        return FeedbackCollector(trubrics_platform_auth="multiple_users")

    collector = trubrics_init()

    with st.sidebar:
        collector.st_trubrics_auth()

    collector.st_feedback(feedback_type="issue")
    ```

    !!!Note
        As streamlit refreshes your app on each interaction, make use of st.cache to save authentication information for the session.
