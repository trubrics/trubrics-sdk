import dash_bootstrap_components as dbc
from dash import Dash, html

from trubrics.integrations.dash import collect_feedback

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([collect_feedback(tags=["Dash"], save_ui=False)])

if __name__ == "__main__":
    app.run_server(debug=True)
