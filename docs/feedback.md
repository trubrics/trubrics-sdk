# Gather feedback from business users

Trubrics feedback components help you to collect feedback on your models with your favourite python library. Once feedback has been collected from business users, it should be translated into validation points to ensure repeatable checking throughout the lifetime of the model. Add the trubrics feedback component to your ML apps now to start collecting feedback:

<table>
<tr>
<th> Framework </th>
<th style="text-align:center"> Getting Started Code Snippets </th>
</tr>
<tr>
<td>

[Streamlit](https://streamlit.io/)

</td>
<td>

```py
from trubrics.feedback import collect_feedback_streamlit

collect_feedback_streamlit(
    path=".",  # path to feedback .json file
    file_name=None,  # file name, if None defaults to feedback.json
    metadata=None,  # a dict of any metadata to save from you app
    tags=None  # a list of any tags for this feedback file
)
```

</td>
</tr>
<tr>
<td>

[Dash](https://dash.plotly.com/)

</td>

<td>

```py
from dash import Dash, html

from trubrics.feedback import collect_feedback_dash

app = Dash(__name__)

app.layout = html.Div(
    [
        collect_feedback_dash(
            path=".",  # path to feedback .json file
            file_name=None,  # file name, if None defaults to feedback.json
            metadata=None,  # a dict of any metadata to save from you app
            tags=None  # a list of any tags for this feedback file
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

</td>
</tr>
<tr>
<td>

[Gradio](https://gradio.app/)

</td>
<td>

```py
import gradio as gr

from trubrics.feedback import collect_feedback_gradio

with gr.Blocks() as demo:
    collect_feedback_gradio(
        path=".",  # path to feedback .json file
        file_name=None,  # file name, if None defaults to feedback.json
        metadata=None,  # a dict of any metadata to save from you app
        tags=None  # a list of any tags for this feedback file
    )

demo.launch()
```

</td>
</tr>
</table>

You can view our demo user feedback app, using the streamlit feedback collector and an example experimentation tool, on the titanic dataset & model on [Hugging Face Spaces](https://huggingface.co/spaces/trubrics/trubrics-titanic-demo), or run it locally with the CLI command:

```console
(venv)$ trubrics example-app
```

![img](assets/titanic-feedback-example.png)
