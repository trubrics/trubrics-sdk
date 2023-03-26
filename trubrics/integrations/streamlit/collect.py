from typing import Any, Dict, List, Optional, Tuple, Union

import streamlit as st

from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback
from trubrics.ui.auth import get_trubrics_auth_token
from trubrics.ui.trubrics_config import load_trubrics_config


class FeedbackCollector:
    def __init__(
        self,
        data: Optional[str] = None,
        model: Optional[str] = None,
        trubrics_platform_auth: Optional[str] = None,
    ):
        """
        The FeedbackCollector allows Data Scientists to collect feedback from with their app.

        Args:
            data: a reference to the data that was used to collect the feedback (e.g. a link to a dataset)
            model: a reference to the model that was used to collect the feedback (e.g. a link to a model)
            trubrics_platform_auth: option to save the feedback to the trubrics platform

                - *None*: save feedback locally to .json
                - *single_user*: save feedback directly to the Trubrics platform,
                    using auth credentials of the app owner
                - *multiple_users*: save feedback directly to the Trubrics platform, with full user auth
        """
        self.data = data
        self.model = model
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
        user_response: Optional[Dict[str, Union[float, int, str, bool]]] = None,
        path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        key: Optional[str] = None,
        open_feedback_label: Optional[str] = None,
    ) -> Optional[Feedback]:
        """
        Collect user feedback within a Streamlit web application.

        Args:
            type: type of feedback to be collected

                - issue: issue with a open text title and description fields
                - thumbs: positive or negative feedback with thumbs emojis
                - faces: a scale of 1 to 5 with face emojis
                - custom: any custom title and description str
            user_response: a dict of user responses to save with your feedback
            path: path to save feedback local .json. Defaults to "./*timestamp*_feedback.json"
            metadata: data to save with your feedback
            tags: a list of tags for your feedback
            key: a key for each streamlit component
            open_feedback_label: label of optional text_input for "faces" or "thumbs" type
        """
        if key is None:
            key = type
        if type == "issue":
            if user_response or open_feedback_label:
                raise ValueError("For type='issue', title, description and open_feedback_label must be None.")
            issue_data = self.st_issue_ui(key)
            if issue_data:
                return self._save_feedback(
                    type=type,
                    path=path,
                    metadata=metadata,
                    user_response={issue_data[0]: issue_data[1]},
                    tags=tags,
                )
        elif type in ("thumbs", "faces"):
            if user_response:
                raise ValueError(f"For type='{type}', user_response is set inside the component (must be None).")
            return self._save_quantitative_feedback(
                type=type,
                path=path,
                metadata=metadata,
                tags=tags,
                key=key,
                open_feedback_label=open_feedback_label,
            )
        elif type == "custom":
            if user_response:
                return self._save_feedback(
                    type=type,
                    user_response=user_response,
                    path=path,
                    metadata=metadata,
                    tags=tags,
                )
            else:
                raise ValueError("For type='custom', title and description parameters must be specified.")
        else:
            raise ValueError("type must be one of ['issue', 'faces', 'thumbs', 'custom'].")
        return None

    def _save_feedback(
        self,
        type: str,
        user_response: Dict[str, Union[float, int, str, bool]],
        path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Feedback]:
        feedback = Feedback(
            type=type,
            user_response=user_response,
            data=self.data,
            model=self.model,
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
        return feedback

    def _save_quantitative_feedback(
        self,
        type,
        key,
        open_feedback_label: Optional[str],
        path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Feedback]:
        if f"{key}_state" not in st.session_state:
            st.session_state[f"{key}_state"] = ""
        if f"{key}_save_button" not in st.session_state:
            st.session_state[f"{key}_save_button"] = False
        if f"previous_{key}_state" not in st.session_state:
            st.session_state[f"previous_{key}_state"] = ""

        title = f"User satisfaction: {type}"

        def feedback_handler(open_feedback_label):
            user_response = {
                title: st.session_state[f"{key}_state"],
                open_feedback_label: st.session_state[f"{type}_open_feedback"].rstrip(),
            }
            st.session_state[f"previous_{key}_state"] = user_response
            st.session_state[f"{key}_state"] = ""

            # re-enable all buttons
            disabled_keys = [f"{key}_{index}_disable" for index in range(1, 6 if type == "faces" else 3)]
            for disabled_key in disabled_keys:
                st.session_state[disabled_key] = False

        ui_state = getattr(self, f"st_{type}_ui")(key=key, disable_on_click=True if open_feedback_label else False)

        if ui_state or st.session_state[f"{key}_state"]:
            if open_feedback_label:
                if st.session_state[f"{key}_state"] == "":
                    st.session_state[f"{key}_state"] = ui_state
                st.text_input(open_feedback_label, key=f"{type}_open_feedback")
                st.button(
                    config.FEEDBACK_SAVE_BUTTON,
                    on_click=feedback_handler,
                    args=(open_feedback_label,),
                    key=f"{key}_save_button",
                )
            else:
                st.session_state[f"{key}_state"] = ui_state
                user_response = {title: ui_state}
                return self._save_feedback(
                    user_response=user_response, type=type, metadata=metadata, path=path, tags=tags
                )
        if st.session_state[f"{key}_save_button"]:
            user_response = {title: ui_state}
            return self._save_feedback(
                user_response=st.session_state[f"previous_{key}_state"],
                type=type,
                metadata=metadata,
                path=path,
                tags=tags,
            )
        return None

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

    def st_thumbs_ui(self, disable_on_click: bool = False, key: Optional[str] = None) -> Optional[str]:
        if key is None:
            key = "thumbs"

        button_states = [f"{key}_1", f"{key}_2"]
        col1, col2 = st.columns([1, 15])
        with col1:
            up = self._emoji_button("👍", key, disable_on_click, button_states, 1)
        with col2:
            down = self._emoji_button("👎", key, disable_on_click, button_states, 2)
        if up:
            return ":1 - thumbs up:"
        elif down:
            return ":2 - thumbs down:"
        else:
            return None

    def st_faces_ui(self, disable_on_click: bool = False, key: Optional[str] = None) -> Optional[str]:
        if key is None:
            key = "faces"

        button_states = [f"{key}_1", f"{key}_2", f"{key}_3", f"{key}_4", f"{key}_5"]
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 10])
        with col1:
            one = self._emoji_button("😞", key, disable_on_click, button_states, 1)
        with col2:
            two = self._emoji_button("🙁", key, disable_on_click, button_states, 2)
        with col3:
            three = self._emoji_button("😐", key, disable_on_click, button_states, 3)
        with col4:
            four = self._emoji_button("🙂", key, disable_on_click, button_states, 4)
        with col5:
            five = self._emoji_button("😀", key, disable_on_click, button_states, 5)

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

    def _emoji_button(self, emoji, key, disable_on_click, keys, index):
        return st.button(
            emoji,
            key=f"{key}_{index}",
            on_click=self._disable_buttons,
            args=(disable_on_click, index, keys),
            disabled=st.session_state.get(f"{key}_{index}_disable", False),
        )

    @staticmethod
    def _disable_buttons(disable_on_click, index, button_states):
        if disable_on_click:
            enabled = button_states.pop(index - 1)
            st.session_state[enabled + "_disable"] = False
            for button_state in button_states:
                st.session_state[button_state + "_disable"] = True
