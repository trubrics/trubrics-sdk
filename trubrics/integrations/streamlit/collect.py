from typing import Any, Dict, List, Optional, Tuple

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
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        key: Optional[str] = None,
        open_feedback_label: Optional[str] = None,
    ):
        """
        Collect user feedback within a Streamlit web application.

        Args:
            type: type of feedback to be collected

                - issue: issue with a open text title and description fields
                - thumbs: positive or negative feedback with thumbs emojis
                - faces: a scale of 1 to 5 with face emojis
                - custom: any custom title and description str
            metadata: data to save with your feedback
            title: optional title of Feedback
            description: optional description of Feedback
            path: path to save feedback local .json. Defaults to "./*timestamp*_feedback.json"
            tags: a list of tags for your feedback
            key: a key for each streamlit component
            open_feedback_label: label of optional text_input for "faces" or "thumbs" type
        """
        if key is None:
            key = type
        if type == "issue":
            if title or description or open_feedback_label:
                raise ValueError("For type='issue', title, description and open_feedback_label must be None.")
            issue_data = self.st_issue_ui(key)
            if issue_data:
                title, description = issue_data
                self._save_feedback(
                    type=type,
                    path=path,
                    metadata=metadata,
                    title=title,
                    description=description,
                    tags=tags,
                )
        elif type in ("thumbs", "faces"):
            if description:
                raise ValueError(f"For type='{type}', description is set inside the component (must be None).")
            self._save_quantitative_feedback(
                type=type,
                path=path,
                metadata=metadata,
                title=title,
                tags=tags,
                key=key,
                open_feedback_label=open_feedback_label,
            )
        elif type == "custom":
            if not title or not description:
                raise ValueError("For type='custom', title and description parameters must be specified.")
            self._save_feedback(
                type=type,
                path=path,
                metadata=metadata,
                title=title,
                description=description,
                tags=tags,
            )
        else:
            raise ValueError("type must be one of ['issue', 'faces', 'thumbs', 'custom'].")

    def _save_feedback(self, title, description, type, metadata, path, tags):
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

    def _save_quantitative_feedback(self, key, title, open_feedback_label, type, metadata, path, tags):
        if f"{key}_state" not in st.session_state:
            st.session_state[f"{key}_state"] = ""
        title = title or f"User satisfaction: {type}"

        def feedback_handler():
            description = f"{st.session_state[f'{key}_state']} {st.session_state[f'{type}_description']}".rstrip()
            self._save_feedback(title, description, type, metadata, path, tags)
            st.session_state[f"{key}_state"] = ""

        ui_state = getattr(self, f"st_{type}_ui")()

        if ui_state or st.session_state[f"{key}_state"]:
            if open_feedback_label:
                if st.session_state[f"{key}_state"] == "":
                    st.session_state[f"{key}_state"] = ui_state
                st.text_input(open_feedback_label, key=f"{type}_description")
                st.button(config.FEEDBACK_SAVE_BUTTON, on_click=feedback_handler)
            else:
                st.session_state[f"{key}_state"] = ui_state
                self._save_feedback(title, ui_state, type, metadata, path, tags)

    @staticmethod
    def st_issue_ui(key: Optional[str] = None) -> Optional[Tuple[str, str]]:
        if key is None:
            key = "issue"

        if f"{key}_save_button" not in st.session_state:
            st.session_state[f"{key}_save_button"] = False

        if f"previous_{key}_state" not in st.session_state:
            st.session_state[f"previous_{key}_state"] = ""

        def clear_session_state():
            st.session_state[f"previous_{key}_state"] = (
                st.session_state[f"{key}_title"],
                st.session_state[f"{key}_description"],
            )
            st.session_state[f"{key}_title"] = ""
            st.session_state[f"{key}_description"] = ""

        title = st.text_input(
            label=config.TITLE,
            help=config.TITLE_EXPLAIN,
            key=f"{key}_title",
        )
        description = st.text_input(
            label=config.DESCRIPTION,
            help=config.DESCRIPTION_EXPLAIN,
            key=f"{key}_description",
        )
        enabled = title and description
        if enabled:
            st.button(config.FEEDBACK_SAVE_BUTTON, on_click=clear_session_state, key=f"{key}_save_button")
        if st.session_state[f"{key}_save_button"]:
            return st.session_state[f"previous_{key}_state"]
        else:
            return None

    @staticmethod
    def st_thumbs_ui(key: Optional[str] = None) -> Optional[str]:
        if key is None:
            key = "thumbs"
        col1, col2 = st.columns([1, 15])
        with col1:
            up = st.button("👍", key=f"{key}_up")
        with col2:
            down = st.button("👎", key=f"{key}_down")
        if up:
            return ":thumbs up:"
        elif down:
            return ":thumbs down:"
        else:
            return None

    @staticmethod
    def st_faces_ui(key: Optional[str] = None) -> Optional[str]:
        if key is None:
            key = "faces"
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 10])
        with col1:
            one = st.button("😞", key=f"{key}_1")
        with col2:
            two = st.button("🙁", key=f"{key}_2")
        with col3:
            three = st.button("😐", key=f"{key}_3")
        with col4:
            four = st.button("🙂", key=f"{key}_4")
        with col5:
            five = st.button("😀", key=f"{key}_5")
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
