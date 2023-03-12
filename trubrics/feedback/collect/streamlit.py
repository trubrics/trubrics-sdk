from typing import Any, Dict, List, Optional

import streamlit as st

from trubrics.context import DataContext
from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


class FeedbackCollector:
    def __init__(
        self,
        data_context: DataContext,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        tags: Optional[List[str]] = None,
        save_ui: bool = False,
    ):
        self.dc = data_context
        self.model_name = model_name
        self.model_version = model_version
        self.tags = tags
        self.save_ui = save_ui

        if save_ui:
            col1, col2 = st.columns(2)
            with col1:
                self.email = st.text_input(label=config.USER_EMAIL, key="email")
            with col2:
                self.password = st.text_input(label=config.USER_PASSWORD, key="password", type="password")

    def st_feedback(self, path: Optional[str] = None, type: str = "issue", metadata: Optional[Dict[str, Any]] = None):
        """
        Collect user feedback within a Streamlit web application.

        Args:
            path: path to save feedback local .json. Defaults to "./<timestamp>_feedback.json"
            type: type of feedback to be collected
                - issue: issue with a open text title and description fields
                - thumbs: a thumbs up or thumbs down feedback
                - scale: a scale of 1 to n
                - scale_open: a scale of 1 to n with an open text field
                - n_open: n open text fields
        """
        title, description = None, None
        if type == "issue":
            issue_data = self._st_feedback_issue()
            if issue_data:
                title, description = issue_data
        elif type == "thumbs":
            thumbs_data = self._st_feedback_thumbs()
            if thumbs_data:
                title = thumbs_data
                description = "reaction"
        elif type == "faces":
            faces_data = self._st_feedback_faces()
            if faces_data:
                title = faces_data
                description = "reaction"
        else:
            raise NotImplementedError()

        print(title, description)

        if title and description:
            feedback = Feedback(
                title=title,
                description=description,
                data_context_name=self.dc.name,
                data_context_version=self.dc.version,
                metadata=metadata,
            )
            if self.save_ui:
                feedback.save_ui(self.email, self.password)  # type: ignore
            else:
                feedback.save_local(path=path)
            st.success(config.FEEDBACK_SAVED)

    @staticmethod
    def _st_feedback_issue():
        with st.form("form", clear_on_submit=True):
            title = st.text_input(label=config.TITLE, help=config.TITLE_EXPLAIN, key="title")
            description = st.text_input(label=config.DESCRIPTION, help=config.DESCRIPTION_EXPLAIN, key="description")
            submitted = st.form_submit_button(config.FEEDBACK_SAVE_BUTTON)
            if submitted:
                if len(title) == 0 or len(description) == 0:
                    st.error(config.FEEDBACK_NOT_SAVED)
                else:
                    return title, description

    @staticmethod
    def _st_feedback_thumbs():
        col1, col2 = st.columns([1, 15])
        with col1:
            up = st.button("👍")
        with col2:
            down = st.button("👎")
        if up:
            return "up"
        elif down:
            return "down"
        else:
            return None

    @staticmethod
    def _st_feedback_faces():
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 10])
        with col1:
            one = st.button("😞")
        with col2:
            two = st.button("🙁")
        with col3:
            three = st.button("😐")
        with col4:
            four = st.button("🙂")
        with col5:
            five = st.button("😀")
        if one:
            return "1"
        elif two:
            return "2"
        elif three:
            return "3"
        elif four:
            return "4"
        elif five:
            return "5"
        else:
            return None
