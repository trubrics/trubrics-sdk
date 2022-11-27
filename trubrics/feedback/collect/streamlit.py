from typing import Any, Dict, List, Optional

import streamlit as st

from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


def collect_feedback_streamlit(
    path: str,
    file_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
):
    """
    Gets feedback from the user and saves it in the path given through the input through streamlit web user interface.
    Feedback can be in the form of text or any other format. If no path is given, it saves it in the default working directory.

    Args:
        path : The path where the feedback file gets saved. If empty, defaults to current working directory.
        file_name: Name of the file. If Empty,defaults to "Feedback.json"
        metadata: Any other form of metric which the user wants to log into the feedback file such as feature value,prediction,etc. If empty,defaults to None.
        tags: list of any tags for this feedback file. If empty,defaults to None.

    """
    with st.form("form", clear_on_submit=True):
        title = st.text_input(label=config.TITLE, help=config.TITLE_EXPLAIN, key="title")
        description = st.text_input(label=config.DESCRIPTION, help=config.DESCRIPTION_EXPLAIN, key="description")
        submitted = st.form_submit_button(config.FEEDBACK_SAVE_BUTTON)
        if submitted:
            if len(title) == 0 or len(description) == 0:
                st.markdown(
                    config.FEEDBACK_NOT_SAVED_HTML,
                    unsafe_allow_html=True,
                )
            else:
                feedback = Feedback(title=title, description=description, tags=tags, metadata=metadata)
                feedback.save_local(path=path, file_name=file_name)
                st.markdown(
                    config.FEEDBACK_SAVED_HTML,
                    unsafe_allow_html=True,
                )
