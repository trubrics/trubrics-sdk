from typing import Any, Dict, List, Optional

import streamlit as st

from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


def collect_feedback_streamlit(
    path: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    save_ui: bool = False,
):
    """
    A component to collect user feedback within a Streamlit web application.

    Args:
        path: path to save feedback local .json. Defaults to "./<timestamp>_feedback.json"
        metadata: any metric which the user wants to save into the feedback issue such as
                  feature values, prediction, etc. Defaults to None.
        tags: list of any tags for the feedback issue. Defaults to None.
        save_ui: save to the Trubrics platform
    """
    with st.form("form", clear_on_submit=True):
        title = st.text_input(label=config.TITLE, help=config.TITLE_EXPLAIN, key="title")
        description = st.text_input(label=config.DESCRIPTION, help=config.DESCRIPTION_EXPLAIN, key="description")
        if save_ui:
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input(label=config.USER_EMAIL, key="email")
            with col2:
                password = st.text_input(label=config.USER_PASSWORD, key="password", type="password")
        submitted = st.form_submit_button(config.FEEDBACK_SAVE_BUTTON)
        if submitted:
            if len(title) == 0 or len(description) == 0:
                st.markdown(
                    config.FEEDBACK_NOT_SAVED_HTML,
                    unsafe_allow_html=True,
                )
            else:
                feedback = Feedback(title=title, description=description, tags=tags, metadata=metadata)
                if save_ui:
                    feedback.save_ui(email, password)  # type: ignore
                else:
                    feedback.save_local(path=path)
                st.markdown(
                    config.FEEDBACK_SAVED_HTML,
                    unsafe_allow_html=True,
                )
