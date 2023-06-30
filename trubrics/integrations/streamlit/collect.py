from datetime import datetime
from typing import Optional

import streamlit as st

from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback, Response
from trubrics.feedback.save_to_trubrics import save_to_trubrics as save
from trubrics.trubrics_platform.auth import init


class FeedbackCollector:
    def __init__(
        self,
        component_name: str,
        email: Optional[str],
        password: Optional[str],
        firebase_api_key: Optional[str] = None,
        firebase_project_id: Optional[str] = None,
    ):
        """
        Args:
            component_name: the component name that has been created in Trubrics
            email: a Trubrics account email
            password: a Trubrics account password
        """
        self.component_name = component_name
        if email and password:
            self.trubrics_config = init(
                email=email,
                password=password,
                firebase_api_key=firebase_api_key,
                firebase_project_id=firebase_project_id,
            )

    def st_feedback(
        self,
        feedback_type: str,
        model: str,
        tags: list = [],
        metadata: dict = {},
        response: Optional[Response] = None,
        user_id: Optional[str] = None,
        created_on: datetime = datetime.now(),
        key: Optional[str] = None,
        open_feedback_label: Optional[str] = None,
        save_to_trubrics: bool = True,
    ) -> Optional[dict]:
        """
        Collect ML model user feedback with UI components from a Streamlit app.

        Args:
            feedback_type: type of feedback to be collected

                - textbox: open textbox feedback
                - thumbs: 👍 / 👎 UI buttons
                - faces: 😞 / 🙁 / 😐 / 🙂 / 😀 UI buttons
            model: the model used - can be a model version, a link to the saved model artifact in cloud storage, etc
            tags: a list of tags for the feedback
            metadata: any data to save with the feedback
            response: a dict of user responses to save with the feedback for feedback_type='custom'
            user_id: an optional reference to a user, for example a username if there is a login, a cookie ID, etc
            key: a key for the streamlit components (necessary if calling this method multiple times with the same type)
            open_feedback_label: label of optional text_input for "faces" or "thumbs" feedback_type
            save_to_trubrics: whether to save the feedback to Trubrics, or just to return the feedback object
        """
        if key is None:
            key = feedback_type
        if feedback_type == "textbox":
            if response:
                raise ValueError("For feedback_type='textbox', user_response must be None.")
            text = self.st_textbox_ui(key, label=open_feedback_label)
            if text:
                response = Response(type=feedback_type, score=None, text=text)
                return self._save_feedback(
                    model=model,
                    response=response,
                    user_id=user_id,
                    tags=tags,
                    metadata=metadata,
                    created_on=created_on,
                    save_to_trubrics=save_to_trubrics,
                )
        elif feedback_type in ("thumbs", "faces"):
            if response:
                raise ValueError(
                    f"For feedback_type='{feedback_type}', response is set inside the component (must be None)."
                )
            return self._save_quantitative_feedback(
                model=model,
                feedback_type=feedback_type,
                user_id=user_id,
                metadata=metadata,
                tags=tags,
                created_on=created_on,
                key=key,
                open_feedback_label=open_feedback_label,
                save_to_trubrics=save_to_trubrics,
            )
        elif feedback_type == "custom":
            raise NotImplementedError(
                "This is currently not implemented. Get in touch to understand how to save custom feedback."
            )
            # if response:
            #     return self._save_feedback(...)
            # else:
            #     raise ValueError("For feedback_type='custom', title and description parameters must be specified.")
        else:
            raise ValueError("feedback_type must be one of ['textbox', 'faces', 'thumbs', 'custom'].")
        return None

    def _save_feedback(
        self,
        model: str,
        response: Response,
        user_id: Optional[str] = None,
        tags: list = [],
        metadata: dict = {},
        created_on: datetime = datetime.now(),
        save_to_trubrics: bool = True,
    ) -> Optional[dict]:
        feedback = Feedback(
            component_name=self.component_name,
            response=response,
            model=model,
            metadata=metadata,
            tags=tags,
            user_id=user_id,
            created_on=created_on,
        )
        if save_to_trubrics:
            res = save(trubrics_config=self.trubrics_config, feedback=feedback)
            if "error" in res:
                error_msg = f"Error in pushing feedback issue to Trubrics: {res}"
                st.error(error_msg)
            else:
                st.success(config.PLATFORM_SAVE)
        return feedback.dict()

    def _save_quantitative_feedback(
        self,
        feedback_type: str,
        key: str,
        open_feedback_label: Optional[str],
        model: str,
        user_id: Optional[str] = None,
        tags: list = [],
        metadata: dict = {},
        created_on: datetime = datetime.now(),
        save_to_trubrics: bool = True,
    ) -> Optional[dict]:
        if f"{key}_state" not in st.session_state:
            st.session_state[f"{key}_state"] = ""
        if f"{key}_save_button" not in st.session_state:
            st.session_state[f"{key}_save_button"] = False
        if f"previous_{key}_state" not in st.session_state:
            st.session_state[f"previous_{key}_state"] = ""

        def feedback_handler():
            response = Response(
                type=feedback_type,
                score=st.session_state[f"{key}_state"],
                text=st.session_state[f"{feedback_type}_open_feedback_{key}"].rstrip(),
            )
            st.session_state[f"previous_{key}_state"] = response
            st.session_state[f"{key}_state"] = ""

            self._enable_all_buttons(feedback_type=feedback_type)

        ui_state = getattr(self, f"st_{feedback_type}_ui")(
            key=key, disable_on_click=True if open_feedback_label else False
        )
        if ui_state:
            st.session_state[f"{key}_state"] = ui_state

        if open_feedback_label:
            if st.session_state.get(f"{key}_state_clicked", "") != "":
                st.text_input(open_feedback_label, key=f"{feedback_type}_open_feedback_{key}")
                st.button(
                    config.FEEDBACK_SAVE_BUTTON,
                    on_click=feedback_handler,
                    key=f"{key}_save_button",
                )
        else:
            if ui_state:
                response = Response(
                    type=feedback_type,
                    score=ui_state,
                    text=None,
                )
                return self._save_feedback(
                    model=model,
                    response=response,
                    user_id=user_id,
                    tags=tags,
                    metadata=metadata,
                    created_on=created_on,
                    save_to_trubrics=save_to_trubrics,
                )
        if st.session_state[f"{key}_save_button"]:
            return self._save_feedback(
                model=model,
                response=st.session_state[f"previous_{key}_state"],
                user_id=user_id,
                tags=tags,
                metadata=metadata,
                created_on=created_on,
                save_to_trubrics=save_to_trubrics,
            )
        return None

    @staticmethod
    def st_textbox_ui(key: Optional[str] = None, label: Optional[str] = None) -> Optional[str]:
        """
        Trubrics 'textbox' UI component.

        Args:
            key: a key for the streamlit components (necessary if calling this method multiple times with the same type)
            label: the textbox's streamlit label
        """
        if key is None:
            key = "textbox"

        if f"{key}_save_button" not in st.session_state:
            st.session_state[f"{key}_save_button"] = False

        if f"previous_{key}_state" not in st.session_state:
            st.session_state[f"previous_{key}_state"] = ""

        def clear_session_state():
            st.session_state[f"previous_{key}_state"] = st.session_state[f"{key}_title"]
            st.session_state[f"{key}_title"] = ""

        title = st.text_input(
            label=label or "Provide some feedback",
            key=f"{key}_title",
        )
        if title:
            st.button(config.FEEDBACK_SAVE_BUTTON, on_click=clear_session_state, key=f"{key}_save_button")
        if st.session_state[f"{key}_save_button"]:
            return st.session_state[f"previous_{key}_state"]
        else:
            return None

    def st_thumbs_ui(self, disable_on_click: bool = False, key: Optional[str] = None) -> Optional[str]:
        """
        Trubrics 'thumbs' UI component - two thumbs buttons.

        Args:
            disable_on_click: disable all other buttons when a button is clicked
            key: a key for the streamlit components (necessary if calling this method multiple times with the same type)
        """
        if key is None:
            key = "thumbs"

        button_states = [f"{key}_1", f"{key}_2"]
        col1, col2 = st.columns([1, 15])
        with col1:
            up = self._emoji_button("👍", key, disable_on_click, button_states, 1)
        with col2:
            down = self._emoji_button("👎", key, disable_on_click, button_states, 2)

        if up:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 1, "👍")
        elif down:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 2, "👎")
        else:
            return None

    def st_faces_ui(self, disable_on_click: bool = False, key: Optional[str] = None) -> Optional[str]:
        """
        Trubrics 'faces' UI component - two thumbs buttons.

        Args:
            disable_on_click: disable all other buttons when a button is clicked
            key: a key for the streamlit components (necessary if calling this method multiple times with the same type)
        """
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
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 1, "😞")
        elif two:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 2, "🙁")
        elif three:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 3, "😐")
        elif four:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 4, "🙂")
        elif five:
            return self._return_quantitative_ui_button(key, disable_on_click, button_states, 5, "😀")
        else:
            return None

    @staticmethod
    def _return_quantitative_ui_button(ui_type, disable_on_click, button_states, index, output):
        if disable_on_click:
            if st.session_state[f"{ui_type}_state_clicked"] == button_states[index - 1]:
                return output
            else:
                return None
        else:
            return output

    def _emoji_button(self, emoji, key, disable_on_click, button_states, index):
        return st.button(
            emoji,
            key=f"{key}_{index}",
            on_click=self._disable_buttons,
            args=(key, disable_on_click, index, button_states),
            disabled=st.session_state.get(f"{key}_{index}_disable", False),
        )

    @staticmethod
    def _disable_buttons(key, disable_on_click, index, button_states):
        """Disable all buttons except the one that was clicked, and re-enable all buttons if re-clicked."""
        if disable_on_click:
            if any([st.session_state.get(button_state + "_disable", False) for button_state in button_states]):
                st.session_state[f"{key}_state_clicked"] = ""
                for button_state in button_states:
                    st.session_state[button_state + "_disable"] = False
            else:
                enabled = button_states.pop(index - 1)
                st.session_state[enabled + "_disable"] = False
                st.session_state[f"{key}_state_clicked"] = enabled
                for button_state in button_states:
                    st.session_state[button_state + "_disable"] = True

    @staticmethod
    def _enable_all_buttons(feedback_type):
        for key in st.session_state:
            if key.endswith("_disable") and key.startswith(feedback_type):
                st.session_state[key] = False
            if key == f"{feedback_type}_state_clicked":
                st.session_state[key] = ""
