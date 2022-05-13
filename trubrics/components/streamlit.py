from typing import Union

import pandas as pd
import streamlit as st

from trubrics.utils.loader import save_test_to_json


def feedback(
    prediction: Union[str, int],
    df: pd.DataFrame,
):
    """get user feedback and save"""
    st.title("Send feedback to the data team:")
    test = st.selectbox(
        "Choose Feedback type:",
        (
            "Single Edge Case",
            "Bias",
            "Other",
        ),
    )

    if test == "Other":
        description = st.text_input(
            "Send personalized feedback",
            'Model is always predicting "die" for all male passengers?',
        )
        corrected_prediction = None
    elif test == "Single Edge Case":
        st.write(
            "You are signaling that the combination of all features above is a critical"
            " edge case that we must test for."
        )
        corrected_prediction = st.selectbox(
            "The prediction above should be:",
            (
                0,
                1,
            ),
        )
        description = "A single edge case."
    elif test == "Bias":
        corrected_prediction = None
        description = "Feedback on bias."

    if st.button("Send feedback"):
        if corrected_prediction:
            save_test_to_json(
                test=test,
                description=description,
                prediction=prediction,
                df=df,
                corrected_prediction=corrected_prediction,
                tracking=False,
            )
        else:
            save_test_to_json(
                test=test,
                description=description,
                prediction=prediction,
                df=df,
                tracking=False,
            )
        st.balloons()
