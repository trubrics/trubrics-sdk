import gradio as gr

from trubrics.feedback.dataclass import Feedback


def collect_feedback_gradio(title: str, description: str, tags=None, metadata=None):
    if not (len(title) == 0 or len(description) == 0):
        feedback = Feedback(title=title, description=description, tags=tags, metadata=metadata)
        path = "."
        file_name = "feedback.json"
        feedback.save_local(path=path, file_name=file_name)
        return '<p style="color:Green;">Feedback saved & sent to the Data Science team.</p>'
    else:
        return '<p style="color:Red;">Please specify a feedback title and a description.</p>'


with gr.Blocks() as demo:
    gr.Markdown("Gradio app to collect user feedback on models.")
    with gr.Tabs():
        with gr.TabItem("Collect feedback"):
            title = gr.Textbox(label="Title", placeholder="Give the issue an explicit title.")
            description = gr.Textbox(label="Description", placeholder="Detail the issue you have observed.", lines=5)
            out = gr.HTML()
            feedback_button = gr.Button("Send feedback")
    feedback_button.click(collect_feedback_gradio, inputs=[title, description], outputs=out)

demo.launch()
