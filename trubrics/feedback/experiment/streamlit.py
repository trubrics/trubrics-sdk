import pandas as pd
import streamlit as st

from trubrics.context import DataContext


def generate_what_if_streamlit(data_context: DataContext):
    """
    Generate a what-if tool based on the testing_data of the DataContext.
    """
    out_df = pd.DataFrame()
    wi_data = data_context.testing_data
    for col in wi_data.columns:
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
            out_df[col] = [st.selectbox(renamed_col, tuple(series.dropna().unique()))]
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
    data_view = st.selectbox(label="", options=("View full test set", "View test set errors", "View split by target"))
    if data_view == "View full test set":
        st.dataframe(data_context.renamed_testing_data)
    elif data_view == "View test set errors":
        st.dataframe(
            _filter_testing_data_errors(data_context=data_context, model=model).rename(data_context.business_columns)
        )
    elif data_view == "View split by target":
        target_split = st.radio(label="", options=data_context.testing_data[data_context.target].unique())
        st.dataframe(data_context.testing_data.loc[lambda x: x[data_context.target] == target_split])


def _filter_testing_data_errors(data_context, model):
    predict_col = f"{data_context.target}_predictions"
    assign_kwargs = {predict_col: model.predict(data_context.testing_data)}
    return data_context.testing_data.assign(**assign_kwargs).loc[lambda x: x[data_context.target] != x[predict_col], :]
