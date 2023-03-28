from typing import Any, Dict, List, Optional

import dash_bootstrap_components as dbc
from dash import Input, Output, callback, callback_context, html

from trubrics.context import DataContext
from trubrics.feedback import config
from trubrics.feedback.dataclass import Feedback


def collect_feedback(
    path: Optional[str] = None,
    data_context: Optional[DataContext] = None,
    model_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    save_ui: bool = False,
):
    """
    A component to collect user feedback within a Dash web application.

    Args:
        path: path to save feedback local .json. Defaults to "./<timestamp>_feedback.json"
        data_context: the DataContext containing your datasets
        model_name: optional name of your model
        model_version: optional version of your model
        metadata: any metric which the user wants to save into the feedback issue such as
                  feature values, prediction, etc. Defaults to None.
        tags: list of any tags for the feedback issue. Defaults to None.
        save_ui: save to the Trubrics platform
    """
    title_input = html.Div(
        [
            dbc.Label(config.TITLE, html_for="title"),
            dbc.Input(id="title", placeholder=config.TITLE_EXPLAIN),
        ],
        className="mb-3",
    )

    description_input = html.Div(
        [
            dbc.Label(config.DESCRIPTION, html_for="description"),
            dbc.Input(id="description", placeholder=config.DESCRIPTION_EXPLAIN),
        ],
        className="mb-3",
    )

    button = html.Div(
        [
            html.Div(),
            dbc.Button(config.FEEDBACK_SAVE_BUTTON, id="button_input", color="secondary"),
            html.P(id="message"),
        ],
        className="mb-3",
    )

    @callback(
        Output("message", "children"),
        Output("message", "style"),
        Output("title", "value"),
        Output("description", "value"),
        Input("button_input", "n_clicks"),
        Input("title", "value"),
        Input("description", "value"),
    )
    def on_button_click(n, title, description):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        if "button_input" in changed_id:
            if title is None or description is None:
                return config.FEEDBACK_NOT_SAVED, {"color": "Red"}, title, description
            else:
                feedback = Feedback(
                    feedback_type="issue",
                    user_response={title: description},
                    data=data_context.name if data_context else None,
                    model=model_name,
                    metadata=metadata,
                    tags=tags,
                )
                feedback.save_local(path=path)
                if save_ui:
                    raise NotImplementedError()
                    # feedback.save_ui()
                return config.LOCAL_SAVE, {"color": "Green"}, None, None
        else:
            return None, None, title, description

    return dbc.Form([title_input, description_input, button])
