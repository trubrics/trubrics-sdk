import pandas as pd
import streamlit as st

from trubrics.context import DataContext


def generate_what_if_streamlit(data_context: DataContext):
    """
    Generate a what-if tool based on the testing_data of the DataContext.
    """
    out_df = pd.DataFrame()
    wi_data = data_context.testing_data
    if data_context.features:
        for col in data_context.features:
            series = wi_data[col]
            if data_context.business_columns is not None and col in data_context.business_columns.keys():
                renamed_col = data_context.business_columns[col]
            else:
                renamed_col = col
            if data_context.categorical_columns is None:
                raise ValueError(
                    "A list of categorical_columns must be specified in the DataContext for the what-if functionality."
                )
            if col in data_context.categorical_columns:
                out_df[col] = [st.selectbox(label=renamed_col, options=tuple(series.dropna().unique()))]
            else:
                out_df[col] = [
                    st.slider(
                        renamed_col,
                        min_value=int(series.min()),
                        max_value=int(series.max()),
                        value=round(series.mean()),
                    )
                ]
    return out_df


def explore_testing_data(data_context, model):
    test_set = "Full test set"
    test_set_errors = "Test set errors"
    filtered_target = "Filtered prediction value"
    data_view = st.selectbox(
        label="Which data would you like to view?",
        options=[test_set, test_set_errors, filtered_target],
        label_visibility="collapsed",
    )
    if data_view == test_set:
        st.dataframe(data_context.renamed_testing_data)
    elif data_view == test_set_errors:
        st.dataframe(
            _filter_testing_data_errors(data_context=data_context, model=model).rename(data_context.business_columns)
        )
    elif data_view == filtered_target:
        target_split = st.radio(
            label="Prediction value",
            options=data_context.testing_data[data_context.target].unique(),
            label_visibility="collapsed",
        )
        st.dataframe(data_context.testing_data.loc[lambda x: x[data_context.target] == target_split])


def _filter_testing_data_errors(data_context, model):
    predict_col = f"{data_context.target}_predictions"
    assign_kwargs = {predict_col: model.predict(data_context.testing_data)}
    return data_context.testing_data.assign(**assign_kwargs).loc[lambda x: x[data_context.target] != x[predict_col], :]
