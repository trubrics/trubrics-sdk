from typing import Any, Dict, List, Optional

import streamlit as st

from trubrics.context import DataContext
from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback
from trubrics.ui.auth import get_trubrics_auth_token
from trubrics.ui.trubrics_config import load_trubrics_config


class FeedbackCollector:
    def __init__(
        self,
        data_context: DataContext,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        save_ui: bool = False,
        allow_public_feedback: bool = False,
    ):
        self.dc = data_context
        self.model_name = model_name
        self.model_version = model_version
        self.save_ui = save_ui
        self.allow_public_feedback = allow_public_feedback
        self.email = ""
        self.password = ""
        self.authenticated = False

        if not self.save_ui and self.allow_public_feedback:
            raise ValueError(
                "The public feedback argument is only valid when saving to the Trubrics platform. It must also be"
                " accompanied by save_ui=True."
            )

    def st_trubrics_auth(self):
        if self.allow_public_feedback:
            raise ValueError(
                "Allowing public feedback results in all feedback being saved to Trubrics with your credentials. The"
                " `st_trubrics_auth` method is therefore disabled for this option."
            )

        trubrics_config = load_trubrics_config()
        if self.authenticated:
            if st.button("Sign out"):
                self.authenticated = False
                self.st_trubrics_auth()
        else:
            if self.save_ui:
                with st.form("auth form"):
                    self.email = st.text_input(
                        label=config.USER_EMAIL,
                        placeholder=config.USER_EMAIL,
                        label_visibility="collapsed",
                        key="email",
                    )
                    self.password = st.text_input(
                        label=config.USER_PASSWORD,
                        placeholder=config.USER_PASSWORD,
                        label_visibility="collapsed",
                        key="password",
                        type="password",
                    )
                    submitted = st.form_submit_button("Sign In")
                    if submitted:
                        # check auth
                        auth = get_trubrics_auth_token(trubrics_config.firebase_auth_api_url, self.email, self.password)
                        if "error" in auth:
                            st.error(f"Error authenticating user {self.email}. Try again or contact your admin team.")
                        else:
                            st.success(f"{self.email} successfully signed in.")
                            self.authenticated = True
            else:
                raise ValueError(
                    "Please set save_ui=True in FeedbackCollector to use Trubrics authentication to save feedback."
                )

    def st_feedback(
        self,
        path: Optional[str] = None,
        type: str = "issue",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Collect user feedback within a Streamlit web application.

        Args:
            path: path to save feedback local .json. Defaults to "./<timestamp>_feedback.json"
            type: type of feedback to be collected
                - issue: issue with a open text title and description fields
                - thumbs: positive or negative feedback with thumbs emojis
                - faces: a scale of 1 to 5 with face emojis
            metadata: data to save with your feedback
            tags: a list of tags for your feedback
        """
        title, description = None, None
        if type == "issue":
            issue_data = self._st_feedback_issue()
            if issue_data:
                title, description = issue_data
        elif type == "thumbs":
            thumbs_data = self._st_feedback_thumbs()
            if thumbs_data:
                title = "User satisfaction: thumbs"
                description = thumbs_data
        elif type == "faces":
            faces_data = self._st_feedback_faces()
            if faces_data:
                title = "User satisfaction: faces"
                description = faces_data
        else:
            raise ValueError("type must be one of ['issue', 'faces', 'thumbs'].")

        if title and description:
            feedback = Feedback(
                type=type,
                title=title,
                description=description,
                data_context_name=self.dc.name,
                data_context_version=self.dc.version,
                model_name=self.model_name,
                model_version=self.model_version,
                metadata=metadata,
                tags=tags,
            )
            if self.save_ui:
                if self.allow_public_feedback:
                    feedback.save_ui(None, None)
                else:
                    feedback.save_ui(self.email, self.password)
            else:
                feedback.save_local(path=path)
            st.success(config.FEEDBACK_SAVED)

    @staticmethod
    def _st_feedback_issue():
        with st.form("issue form", clear_on_submit=True):
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
            return ":thumbs up:"
        elif down:
            return ":thumbs down:"
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
            return ":very negative:"
        elif two:
            return ":negative:"
        elif three:
            return ":neutral:"
        elif four:
            return ":positive:"
        elif five:
            return ":very positive:"
        else:
            return None
