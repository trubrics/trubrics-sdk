import gradio as gr

from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


def collect_feedback_gradio(path: str, file_name=None, tags=None, metadata=None):
    def get_feedback(title: str, description: str):
        if not (len(title) == 0 or len(description) == 0):
            feedback = Feedback(title=title, description=description, tags=tags, metadata={"tags": ["some tag"]})
            feedback.save_ui()
            return config.FEEDBACK_SAVED_HTML
        else:
            return config.FEEDBACK_NOT_SAVED_HTML

    title = gr.Textbox(label=config.TITLE, placeholder=config.TITLE_EXPLAIN)
    description = gr.Textbox(label=config.DESCRIPTION, placeholder=config.DESCRIPTION_EXPLAIN, lines=5)
    feedback_button = gr.Button(config.FEEDBACK_SAVE_BUTTON)
    kwargs = {"fn": get_feedback, "inputs": [title, description], "outputs": gr.HTML()}
    return feedback_button.click(**kwargs)
