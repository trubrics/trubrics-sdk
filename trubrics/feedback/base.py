from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype

from trubrics.context import DataContext, TrubricsModel
from trubrics.exceptions import PandasSchemaError
from trubrics.feedback.dataclass import Feedback
from trubrics.utils.pandas import schema_is_equal


class FeedbackCollector:
    def __init__(self, data: DataContext, model: Any, feedback_tags: Optional[List[str]] = None):
        self.trubrics_model = TrubricsModel(data=data, model=model)
        self.tags = feedback_tags
        self.what_if_df = None
        self.what_if_prediction = None

    def generate_what_if(self, wi_data: Optional[pd.DataFrame] = None):
        """
        Generate a what-if tool based on a DataFrame input.
        If no DataFrame specified, the DataContext testing data is used.

        TODO: check if total columns > N, option to select top n features based on dict of feature importance
        """
        if wi_data is None:
            wi_data = self.trubrics_model.data.X_test
        else:
            if not schema_is_equal(wi_data, self.trubrics_model.data.testing_data):
                raise PandasSchemaError("Schemas of provided data and X_test in DataContext are different.")

        out_df = pd.DataFrame()
        for col, dtype in wi_data.dtypes.to_dict().items():
            series = wi_data[col]
            if (
                self.trubrics_model.data.business_columns is not None
                and col in self.trubrics_model.data.business_columns.keys()
            ):
                renamed_col = self.trubrics_model.data.business_columns[col]
            else:
                renamed_col = col
            if self.trubrics_model.data.categorical_columns is None:
                raise ValueError(
                    "A list of categorical_columns must be specified in the DataContext for the What-If tool."
                )
            if col in self.trubrics_model.data.categorical_columns:
                if is_numeric_dtype(dtype.type):
                    out_df[col] = [
                        st.slider(
                            renamed_col,
                            min_value=int(series.min()),
                            max_value=int(series.max()),
                            value=round(series.mean()),
                        )
                    ]
                else:
                    out_df[col] = [st.selectbox(renamed_col, tuple(series.dropna().unique()))]
            elif is_numeric_dtype(dtype.type):
                out_df[col] = [
                    st.number_input(
                        renamed_col,
                        min_value=int(series.min()),
                        max_value=int(series.max()),
                        value=int(series.mean()),
                        step=None,
                    )
                ]
            else:
                raise NotImplementedError(f"Columns '{col}' type is not recognised.")
        self.what_if_df = out_df
        self.what_if_prediction = self.trubrics_model.model.predict(out_df)[0]

    def save_feedback(self, path: str, file_name: str):
        """Get user feedback and save."""
        metadata: Dict[str, Any] = {}
        if self.what_if_df is not None:
            what_if_input = self.what_if_df.to_dict("records")[0]
            metadata["what_if_input"] = what_if_input
            metadata["model_prediction"] = self.what_if_prediction

        with st.form("form", clear_on_submit=True):
            title = st.text_input(label="Title", help="Give the issue an explicit title.", key="title")
            description = st.text_input(
                label="Description", help="Detail the issue you have observed.", key="description"
            )
            submitted = st.form_submit_button("Send feedback")
            if submitted:
                if len(title) == 0 or len(description) == 0:
                    st.markdown(
                        '<p style="color:Red;">Please specify a feedback title and a description.</p>',
                        unsafe_allow_html=True,
                    )
                else:
                    single_test = Feedback(title=title, description=description, tags=self.tags, metadata=metadata)
                    single_test.save_local(path=path, file_name=file_name)
                    st.markdown(
                        '<p style="color:Green;">Feedback saved & sent to the Data Science team.</p>',
                        unsafe_allow_html=True,
                    )
