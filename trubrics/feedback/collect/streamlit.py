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
    """Get user feedback and save."""
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
