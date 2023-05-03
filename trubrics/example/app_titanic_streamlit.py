from typing import Optional

import streamlit as st
import typer

from trubrics.cli.main import init
from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.integrations.streamlit import (
    FeedbackCollector,
    generate_what_if_streamlit,
)

cli = typer.Typer()


@st.cache(allow_output_mutation=True)
def init_trubrics(trubrics_platform_auth):
    with st.spinner("Connecting to the Trubrics platform..."):
        init(project_name="LLM demo")
        _, test_df, model = get_titanic_data_and_model()

    data_context = DataContext(
        testing_data=test_df,
        target="Survived",
        categorical_columns=tc.CATEGORICAL_COLUMNS,
        business_columns=tc.BUSINESS_COLUMNS,
    )

    collector = FeedbackCollector(
        data="trubrics data_context",
        model="rf_model",
        trubrics_platform_auth=trubrics_platform_auth,
    )
    return model, data_context, collector


def feedback_example(feedback_type, collector, metadata, open_feedback_label=None, user_response=None):
    file_name = f"{feedback_type}_feedback.json"
    if user_response:
        feedback = collector.st_feedback(
            feedback_type=feedback_type, metadata=metadata, path=file_name, user_response=user_response
        )
    else:
        code_snippet = f"""
        from trubrics.integrations.streamlit import FeedbackCollector
collector = FeedbackCollector()
collector.st_feedback(
    feedback_type="{feedback_type}"{f', open_feedback="{open_feedback_label}"' if open_feedback_label else ''}
)
        """
        feedback = collector.st_feedback(
            feedback_type=feedback_type, metadata=metadata, path=file_name, open_feedback_label=open_feedback_label
        )
        with st.expander(f"See code snippet for feedback_type='{feedback_type}'"):
            st.code(code_snippet)
    if feedback:
        st.write("Example of the FeedbackCollector's output:")
        st.write(feedback.dict())
        st.download_button("Download this example .json file", feedback.json(), mime="text/json", file_name=file_name)
        st.markdown(
            """
            As you collect feedback, .json files are saved to either you local filesystem, or to the Trubrics platform
            (see [here](https://trubrics.github.io/trubrics-sdk/feedback/) for more info).
            """
        )
    st.markdown("***")


@cli.command()
def main(trubrics_platform_auth: Optional[str] = None):
    with st.sidebar:
        if trubrics_platform_auth is None:
            trubrics_platform_auth = st.selectbox(
                label="Select whether to save user feedback locally or to the Trubrics platform: ",
                options=("local", "single_user", "multiple_users"),
            )
            if trubrics_platform_auth == "local":
                trubrics_platform_auth = None
    model, data_context, collector = init_trubrics(trubrics_platform_auth)

    st.title("Titanic Demo App")
    with st.expander("Notes on the demo"):
        st.markdown(
            """
        The sidebar of features and the '**Model prediction**' section below are not a part
        of the FeedbackCollector, but rather a demo of a basic application of how
        you could allow users to test your model and provide feedback.
        """
        )

    with st.sidebar:
        if trubrics_platform_auth == "multiple_users":
            st.title("Authentication")
            collector.st_trubrics_auth()
        st.title("Test the model with different inputs")
        df = generate_what_if_streamlit(data_context=data_context)
    wi_prediction = model.predict(df)[0]

    metadata = {"data": df.to_dict(), "prediction": wi_prediction}

    prediction = "## " + str(wi_prediction) + f"{' (survived)' if wi_prediction else  ' (did not survive)'}"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Model prediction:")
    with col2:
        st.markdown(prediction, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")
    st.markdown("## FeedbackCollector Examples")
    st.markdown(
        """
        Here are examples of how you could implement different types of feedback within your app. Each
        feedback component is:
        - Independent, and can be duplicated around your app
        - Able to collect different data from a specific part of your app
        - Saved to your local filesystem, with a customisable path
        """
    )
    st.markdown("***")

    st.markdown('##### 1 - "Does this prediction look correct?"')
    thumbs_open_feedback = st.radio(
        "Add open feedback?",
        ("No open feedback", "With open feedback"),
        label_visibility="collapsed",
        key="thumbs_radio",
        horizontal=True,
    )
    if thumbs_open_feedback == "With open feedback":
        feedback_example(
            "thumbs", collector=collector, metadata=metadata, open_feedback_label="Please provide a description"
        )
    elif thumbs_open_feedback == "No open feedback":
        feedback_example("thumbs", collector=collector, metadata=metadata)
    else:
        raise NotImplementedError()

    st.markdown('##### 2 - "How satisfied are you with this prediction?"')
    faces_open_feedback = st.radio(
        "Add open feedback?",
        ("No open feedback", "With open feedback"),
        label_visibility="collapsed",
        key="faces_radio",
        horizontal=True,
    )
    if faces_open_feedback == "With open feedback":
        feedback_example(
            "faces", collector=collector, metadata=metadata, open_feedback_label="Please provide a description"
        )
    elif faces_open_feedback == "No open feedback":
        feedback_example("faces", collector=collector, metadata=metadata)
    else:
        raise NotImplementedError()

    st.markdown('##### 3 - "Raise a specific issue"')
    feedback_example("issue", collector=collector, metadata=metadata)

    custom_question = "How much do you love this component?"
    st.markdown(f'##### 4 - "{custom_question}"')
    slider = st.slider("Custom feedback slider", max_value=10, value=9)
    submit = st.button("Save feedback")
    code_snippet = """
    from trubrics.integrations.streamlit import FeedbackCollector
import streamlit as st

collector = FeedbackCollector()

slider = st.slider("Custom feedback slider", max_value=10, value=9)
submit = st.button("Save feedback")

if submit and slider:
    collector.st_feedback(
        "custom",
        user_response={
            "How much do you love this component?": slider,
        }
    )
        """
    with st.expander("See code snippet for feedback_type='custom'"):
        st.code(code_snippet)
    if submit and slider:
        feedback_example(
            "custom",
            collector=collector,
            metadata=metadata,
            user_response={
                custom_question: slider,
            },
        )


if __name__ == "__main__":
    cli(standalone_mode=False)
