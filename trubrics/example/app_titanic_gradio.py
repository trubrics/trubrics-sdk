import gradio as gr

from trubrics.integrations.gradio import collect_feedback

with gr.Blocks() as demo:
    gr.Markdown("Gradio app to collect user feedback on models.")
    with gr.Tab("Feedback"):
        collect_feedback(tags=["Gradio"], save_ui=False)  # set to True to save feedback to Trubrics

demo.launch()
