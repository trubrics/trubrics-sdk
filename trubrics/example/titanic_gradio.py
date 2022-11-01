import gradio as gr

from trubrics.feedback import collect_feedback_gradio

with gr.Blocks() as demo:
    gr.Markdown("Gradio app to collect user feedback on models.")
    with gr.Tab("Feedback"):
        collect_feedback_gradio(path=".")

demo.launch()
