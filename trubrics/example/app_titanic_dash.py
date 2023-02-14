import dash_bootstrap_components as dbc
from dash import Dash, html

from trubrics.feedback import collect_feedback_dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([collect_feedback_dash(tags=["Dash"], save_ui=False)])

if __name__ == "__main__":
    app.run_server(debug=True)
