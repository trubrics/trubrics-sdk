# Gather feedback from business users

Trubrics feedback components help you to collect feedback on your models with your favourite python library. Once feedback has been collected from business users, it should be translated into validation points to ensure repeatable checking throughout the lifetime of the model.

!!!tip "Trubrics platform access"
    The Trubrics platform will allow you to track all issues, and discuss errors with users and other collaborators. There are also capabilities to close feedback issues by linking to specific validation runs. Creating accounts for users will also allow authentication directly in the FeedbackCollector. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access for you and your team.

Add a FeedbackCollector to your ML apps now to start collecting feedback:

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
    path="./feedback_issue.json",  # path to save feedback .json
    tags=["streamlit"],
    metadata={"some": "metadata"},
    save_ui=False,  # set to True to save feedback to Trubrics
)
```

</td>
</tr>
</table>

<details>
  <summary>Dash and Gradio integrations</summary>

<table>
<tr>
<th> Framework </th>
<th style="text-align:center"> Getting Started Code Snippets </th>
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
        collect_feedback_dash()
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
    collect_feedback_gradio()

demo.launch()
```

</td>
</tr>
</table>
</details>

You can view our demo user feedback app, using the streamlit feedback collector and an example experimentation tool, on the titanic dataset & model on [Hugging Face Spaces](https://huggingface.co/spaces/trubrics/trubrics-titanic-demo), or run it locally with the CLI command:

```console
(venv)$ trubrics example-app
```

<p align="center"><img src="../assets/titanic-feedback-example.png"/></p>
