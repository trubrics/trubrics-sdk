from datetime import datetime
from typing import Optional

import streamlit as st
from streamlit_feedback import streamlit_feedback

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
        created_on: Optional[datetime] = None,
        key: Optional[str] = None,
        open_feedback_label: Optional[str] = None,
        save_to_trubrics: bool = True,
        align: str = "flex-end",
        single_submit: bool = True,
        success_fail_message: bool = True,
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
            align: where to align the feedback component ["flex-end", "center", "flex-start"]
            single_submit: disables re-submission. This prevents users re-submitting feedback for a given prediction
                e.g. for a chatbot.
            success_fail_message: whether to display a st.success / st.error message on feedback submission.
        """
        if key is None:
            key = feedback_type
        if feedback_type == "textbox":
            if response:
                raise ValueError("For feedback_type='textbox', response is set inside the component (must be None).")
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
                    success_fail_message=success_fail_message,
                )
        elif feedback_type in ("thumbs", "faces"):
            if response:
                raise ValueError(
                    f"For feedback_type='{feedback_type}', response is set inside the component (must be None)."
                )
            response = streamlit_feedback(
                feedback_type=feedback_type,
                optional_text_label=open_feedback_label,
                single_submit=single_submit,
                align=align,
                key=key,
            )
            if response:
                return self._save_feedback(
                    model=model,
                    response=Response(**response),
                    user_id=user_id,
                    tags=tags,
                    metadata=metadata,
                    created_on=created_on,
                    save_to_trubrics=save_to_trubrics,
                    success_fail_message=success_fail_message,
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
        created_on: Optional[datetime] = None,
        save_to_trubrics: bool = True,
        success_fail_message: bool = True,
    ) -> Optional[dict]:
        feedback = Feedback(
            component_name=self.component_name,
            response=response,
            model=model,
            metadata=metadata,
            tags=tags,
            user_id=user_id,
        )
        if created_on:
            feedback.created_on = created_on
        if save_to_trubrics:
            res = save(trubrics_config=self.trubrics_config, feedback=feedback)
            if "error" in res:
                error_msg = f"Error in pushing feedback issue to Trubrics: {res}"
                if success_fail_message:
                    st.error(error_msg)
            else:
                if success_fail_message:
                    st.success(config.PLATFORM_SAVE)
        return feedback.dict()

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
