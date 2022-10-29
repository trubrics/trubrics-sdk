from typing import Any, Dict, List, Optional

import streamlit as st

from trubrics.feedback.dataclass import Feedback


def collect_feedback_streamlit(
    path: str,
    file_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
):
    """Get user feedback and save."""
    with st.form("form", clear_on_submit=True):
        title = st.text_input(label="Title", help="Give the issue an explicit title.", key="title")
        description = st.text_input(label="Description", help="Detail the issue you have observed.", key="description")
        submitted = st.form_submit_button("Send feedback")
        if submitted:
            if len(title) == 0 or len(description) == 0:
                st.markdown(
                    '<p style="color:Red;">Please specify a feedback title and a description.</p>',
                    unsafe_allow_html=True,
                )
            else:
                feedback = Feedback(title=title, description=description, tags=tags, metadata=metadata)
                feedback.save_local(path=path, file_name=file_name)
                st.markdown(
                    '<p style="color:Green;">Feedback saved & sent to the Data Science team.</p>',
                    unsafe_allow_html=True,
                )
