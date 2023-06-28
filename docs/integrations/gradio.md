# FeedbackCollector Gradio Integration

To get started with [Gradio](https://gradio.app/), install the additional dependency:

```console
pip install "trubrics[gradio]"
```

And add this to your Gradio app:
```py
import gradio as gr

from trubrics.integrations.gradio import collect_feedback

with gr.Blocks() as demo:
    gr.Markdown("Gradio app to collect user feedback on models.")
    with gr.Tab("Feedback"):
        collect_feedback(tags=["Gradio"])

demo.launch()
```
