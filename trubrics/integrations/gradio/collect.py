from typing import Any, Dict, List, Optional

import gradio as gr

from trubrics.context import DataContext
from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


def collect_feedback(
    path: Optional[str] = None,
    data_context: Optional[DataContext] = None,
    model_name: Optional[str] = None,
    model_version: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    save_ui: bool = False,
):
    """
    A component to collect user feedback within a Gradio web application.

    Args:
        path: path to save feedback local .json. Defaults to "./<timestamp>_feedback.json"
        metadata: any metric which the user wants to save into the feedback issue such as
                  feature values, prediction, etc. Defaults to None.
        tags: list of any tags for the feedback issue. Defaults to None.
        save_ui: save to the Trubrics platform
    """

    def get_feedback(title: str, description: str, email: str, password: str):
        if not (len(title) == 0 or len(description) == 0):
            feedback = Feedback(
                type="issue",
                title=title,
                description=description,
                data_context_name=data_context.name if data_context else None,
                data_context_version=data_context.version if data_context else None,
                model_name=model_name,
                model_version=model_version,
                metadata=metadata,
                tags=tags,
            )
            if save_ui:
                feedback.save_ui(email, password)
            else:
                feedback.save_local(path=path)
            return config.FEEDBACK_SAVED_HTML
        else:
            return config.FEEDBACK_NOT_SAVED_HTML

    title = gr.Textbox(label=config.TITLE, placeholder=config.TITLE_EXPLAIN)
    description = gr.Textbox(label=config.DESCRIPTION, placeholder=config.DESCRIPTION_EXPLAIN, lines=5)
    if save_ui:
        with gr.Row():
            email = gr.Textbox(placeholder=config.USER_EMAIL, show_label=False, type="email")
            password = gr.Textbox(placeholder=config.USER_PASSWORD, show_label=False, type="password")
        inputs = [title, description, email, password]
    else:
        inputs = [title, description]
    feedback_button = gr.Button(config.FEEDBACK_SAVE_BUTTON)
    kwargs = {"fn": get_feedback, "inputs": inputs, "outputs": gr.HTML()}
    return feedback_button.click(**kwargs)
