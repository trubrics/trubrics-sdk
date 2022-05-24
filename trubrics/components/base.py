import logging
from typing import Optional, Union

import pandas as pd
import streamlit as st
from jsonschema import SchemaError
from pandas.api.types import is_numeric_dtype

from trubrics.context import DataContext, ModelContext
from trubrics.utils.loader import save_test_to_json
from trubrics.utils.pandas import schema_is_equal

logger = logging.getLogger(__name__)


class BaseComponent:
    """Base class for UI components."""

    def __init__(self, model: ModelContext, data: DataContext):
        self.model = model
        self.data = data

    def _get_renamed_test_data(self):
        """
        Get test DataFrame with renamed business columns.
        """
        return self.data.testing_data.rename(columns=self.data.business_columns)

    def generate_what_if(self, wi_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Generate a what-if tool based on a DataFrame input.
        If no DataFrame specified, the DataContext testing data is used.

        TODO: check if total columns > N, option to select top n features based on dict of feature importance
        """
        if wi_data is None:
            wi_data = self.data.testing_data.drop(columns=[self.data.target_column])
        else:
            if not schema_is_equal(wi_data, self.data.testing_data):
                raise SchemaError("Schemas of provided data and DataContext testing data are different.")
            else:
                wi_data = wi_data.drop(columns=[self.data.target_column])

        out_df = pd.DataFrame()
        for col, dtype in wi_data.dtypes.to_dict().items():
            series = wi_data[col]
            if self.data.business_columns is not None and col in self.data.business_columns.keys():
                renamed_col = self.data.business_columns[col]
            else:
                renamed_col = col
            if self.data.categorical_columns is None:
                raise ValueError("Categorical columns must be specified for the What-If tool.")
            if col in self.data.categorical_columns:
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
                        step=round((int(series.max()) - int(series.min())) / 10),
                    )
                ]
            else:
                raise NotImplementedError(f"Columns '{col}' type is not recognised.")
        return out_df

    def feedback(self, prediction: Union[str, int], df: pd.DataFrame, tracking: bool = False):
        """Get user feedback and save"""
        st.title("Send model feedback:")
        test = st.selectbox(
            "Choose Feedback type:",
            (
                "Single Edge Case",
                "Bias",
                "Other",
            ),
        )
        corrected_prediction: Union[str, int, float, None] = None
        description: Optional[str] = None
        if test == "Other":
            description = st.text_input(label="", value="Send free text feedback here")
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
            description = "Feedback on bias."

        if st.button("Send feedback"):
            if corrected_prediction is None:
                save_test_to_json(
                    test=test,
                    description=description,
                    prediction=prediction,
                    df=df,
                    corrected_prediction=corrected_prediction,
                    tracking=tracking,
                )
            else:
                save_test_to_json(
                    test=test,
                    description=description,
                    prediction=prediction,
                    df=df,
                    tracking=tracking,
                )
            logger.info(f"Predictions saved {'to Trubrics UI' if tracking else 'locally'}.")
            st.balloons()
