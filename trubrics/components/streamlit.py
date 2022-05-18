from typing import Union

import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype

from trubrics.utils.loader import save_test_to_json


def get_streamlit_mapping(train_df, categoricals, target):
    # TODO: check if categoricals are all in train_df, if not warn
    # TODO: check if total columns > N
    if not target:
        raise Exception("No target variable specified.")
    train_df = train_df.drop(columns=target)
    df = pd.DataFrame()
    for col, dtype in train_df.dtypes.to_dict().items():
        series = train_df[col]
        if col in categoricals:
            if is_numeric_dtype(dtype.type):
                df[col] = [
                    st.slider(col, min_value=int(series.min()), max_value=int(series.max()), value=round(series.mean()))
                ]
            else:
                df[col] = [st.selectbox(col, tuple(series.dropna().unique()))]
        elif is_numeric_dtype(dtype.type):
            df[col] = [
                st.number_input(
                    col,
                    min_value=int(series.min()),
                    max_value=int(series.max()),
                    step=round((int(series.max()) - int(series.min())) / 10),
                )
            ]
        else:
            continue
    return df


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
