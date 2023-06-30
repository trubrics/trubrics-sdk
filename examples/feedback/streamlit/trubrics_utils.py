from datetime import datetime, timedelta, timezone

import streamlit as st


def trubrics_config(default_component: bool = True):
    st.subheader("Input your Trubrics credentials:")
    email = st.text_input(
        label="email", placeholder="email", label_visibility="collapsed", value=st.secrets.get("TRUBRICS_EMAIL", "")
    )

    password = st.text_input(
        label="password",
        placeholder="password",
        label_visibility="collapsed",
        type="password",
        value=st.secrets.get("TRUBRICS_PASSWORD", ""),
    )
    st.write("Don't have an account yet? Create one [here](https://trubrics.streamlit.app/)!")

    if default_component:
        return email, password

    feedback_component = st.text_input(
        label="feedback_component",
        placeholder="Feedback component name",
        label_visibility="collapsed",
    )

    feedback_type = st.radio(
        label="Select the component feedback type:", options=("faces", "thumbs", "textbox"), horizontal=True
    )

    return email, password, feedback_component, feedback_type


def datetime_for_timezone(hours):
    """Get the datetime.now() given a number of hours. E.g for hours=-2, get time now for UTC-2"""
    if hours is not None:
        return datetime.now(tz=timezone(timedelta(hours=hours))).replace(tzinfo=None)
    else:
        return datetime.now()


def trubrics_successful_feedback(feedback):
    st.write(
        ":green[You can now view your feedback] [here](https://trubrics.streamlit.app/), :green[and see the raw"
        " feedback response data here:]"
    )
    st.write(feedback)
