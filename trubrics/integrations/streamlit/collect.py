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
        data_context: Optional[DataContext] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        trubrics_platform_auth: Optional[str] = None,
    ):
        """
        The FeedbackCollector allows Data Scientists to collect feedback from with their app.

        Args:
            data_context: a trubrics DataContext, allowing you to record which datasets this app was build with
            model_name: name of an ML model (if used)
            model_version: version of an ML model (if used)
            trubrics_platform_auth: option to save the feedback to the trubrics platform

                - *None*: save feedback locally to .json
                - *single_user*: save feedback directly to the Trubrics platform,
                    using auth credentials of the app owner
                - *multiple_users*: save feedback directly to the Trubrics platform, with full user auth
        """
        self.data_context_name = data_context.name if data_context else None
        self.data_context_version = data_context.version if data_context else None
        self.model_name = model_name
        self.model_version = model_version
        if trubrics_platform_auth in [None, "single_user", "multiple_users"]:
            self.trubrics_platform_auth = trubrics_platform_auth
        else:
            raise ValueError(
                f"trubrics_platform_auth={trubrics_platform_auth} not recognised. Must be one of [None, 'single_user',"
                " 'multiple_users']."
            )

        self.email = ""
        self.password = ""
        self.authenticated = False

    def st_trubrics_auth(self):
        if self.trubrics_platform_auth is None:
            raise ValueError(
                "The `.st_trubrics_auth()` method is reserved for usage with the Trubrics platform. See the"
                " 'trubrics_platform_auth' argument for authentication options."
            )

        trubrics_config = load_trubrics_config()
        if self.authenticated:
            st.write(self.email + " signed in.")
            if st.button("Sign out"):
                self.authenticated = False
                self.st_trubrics_auth()
        else:
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

    def st_feedback(
        self,
        type: str = "issue",
        path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        unique_key: Optional[str] = None,
    ):
        """
        Collect user feedback within a Streamlit web application.

        Args:
            type: type of feedback to be collected

                - issue: issue with a open text title and description fields
                - thumbs: positive or negative feedback with thumbs emojis
                - faces: a scale of 1 to 5 with face emojis
            metadata: data to save with your feedback
            path: path to save feedback local .json. Defaults to "./*timestamp*_feedback.json"
            tags: a list of tags for your feedback
        """
        title, description = None, None
        if type == "issue":
            issue_data = self._st_feedback_issue(unique_key)
            if issue_data:
                title, description = issue_data
        elif type == "thumbs":
            thumbs_data = self._st_feedback_thumbs(unique_key)
            if thumbs_data:
                title = "User satisfaction: thumbs"
                description = thumbs_data
        elif type == "faces":
            faces_data = self._st_feedback_faces(unique_key)
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
                data_context_name=self.data_context_name,
                data_context_version=self.data_context_version,
                model_name=self.model_name,
                model_version=self.model_version,
                metadata=metadata,
                tags=tags,
            )
            if self.trubrics_platform_auth is None:
                feedback.save_local(path=path)
                st.success(config.LOCAL_SAVE)
            elif self.trubrics_platform_auth == "multiple_users":
                if self.authenticated:
                    feedback.save_ui(self.email, self.password)
                    st.success(config.PLATFORM_SAVE)
                else:
                    st.error("User is not authenticated. Please try again or contact your admin.")
            elif self.trubrics_platform_auth == "single_user":
                feedback.save_ui(None, None)
                st.success(config.PLATFORM_SAVE)
            else:
                raise ValueError(
                    f"trubrics_platform_auth={self.trubrics_platform_auth} not recognised. Must be one of [None,"
                    " 'single_user', 'multiple_users']."
                )

    @staticmethod
    def _st_feedback_issue(unique_key):
        with st.form(clear_on_submit=True, key=f"{unique_key}_form"):
            title = st.text_input(label=config.TITLE, help=config.TITLE_EXPLAIN, key=f"{unique_key}_title")
            description = st.text_input(
                label=config.DESCRIPTION, help=config.DESCRIPTION_EXPLAIN, key=f"{unique_key}_description"
            )
            submitted = st.form_submit_button(config.FEEDBACK_SAVE_BUTTON)
            if submitted:
                if len(title) == 0 or len(description) == 0:
                    st.error(config.FEEDBACK_NOT_SAVED)
                else:
                    return title, description

    @staticmethod
    def _st_feedback_thumbs(unique_key):
        col1, col2 = st.columns([1, 15])
        with col1:
            up = st.button("👍", key=f"{unique_key}_up")
        with col2:
            down = st.button("👎", key=f"{unique_key}_down")
        if up:
            return ":thumbs up:"
        elif down:
            return ":thumbs down:"
        else:
            return None

    @staticmethod
    def _st_feedback_faces(unique_key):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 10])
        with col1:
            one = st.button("😞", key=f"{unique_key}_1")
        with col2:
            two = st.button("🙁", key=f"{unique_key}_2")
        with col3:
            three = st.button("😐", key=f"{unique_key}_3")
        with col4:
            four = st.button("🙂", key=f"{unique_key}_4")
        with col5:
            five = st.button("😀", key=f"{unique_key}_5")
        if one:
            return ":1 - very negative:"
        elif two:
            return ":2 - negative:"
        elif three:
            return ":3 - neutral:"
        elif four:
            return ":4 - positive:"
        elif five:
            return ":5 - very positive:"
        else:
            return None
