# FeedbackCollector Dash Integration

To get started with [Dash](https://dash.plotly.com/), install the additional dependency:

```console
(venv)$ pip install "trubrics[dash]"
```

And add this to your Dash app:
```py
from dash import Dash, html

from trubrics.integrations.dash import collect_feedback

app = Dash(__name__)

app.layout = html.Div([collect_feedback(tags=["Dash"])])

if __name__ == "__main__":
    app.run_server(debug=True)
```
