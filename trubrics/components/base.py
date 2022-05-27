import logging
from typing import Optional, Tuple, Union

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
                        value=int(series.mean()),
                        step=None,
                    )
                ]
            else:
                raise NotImplementedError(f"Columns '{col}' type is not recognised.")
        return out_df

    def feedback(self, prediction: Union[str, int], what_if_df: pd.DataFrame, tracking: bool = False):
        """Get user feedback and save"""
        st.title("Send model feedback:")
        test = st.selectbox(
            "Choose feedback type:",
            (
                "Single prediction error",
                "Bias",
                "Important features",
                "Other",
            ),
        )
        corrected_prediction: Union[str, int, float, None] = None
        description: Optional[str] = None
        if test == "Other":
            description = st.text_input(label="", value="Send free text feedback here")

        elif test == "Single prediction error":
            corrected_prediction, description = self._collect_single_edge_case()

        elif test == "Important features":
            selected_feature, top_n_feature, description = self._collect_important_features_feedback()
            description = f"{description}_{selected_feature}_{top_n_feature}"  # TODO: fix save variables

        elif test == "Bias":
            description = "Feedback on bias."

        else:
            raise NotImplementedError()

        if st.button("Send feedback"):
            if corrected_prediction is None:
                save_test_to_json(
                    test=test,
                    description=description,
                    prediction=prediction,
                    df=what_if_df,
                    corrected_prediction=corrected_prediction,
                    tracking=tracking,
                )
            else:
                save_test_to_json(
                    test=test,
                    description=description,
                    prediction=prediction,
                    df=what_if_df,
                    tracking=tracking,
                )
            logger.info(f"Predictions saved {'to Trubrics UI' if tracking else 'locally'}.")
            st.balloons()

    def _collect_single_edge_case(self) -> Tuple[Union[str, int, None], str]:
        """
        Collect correct prediction for the single edge case flag.
        """
        st.write(
            self.__feedback_type_description(
                "you are signalling that the combination of all features is a critical edge case that we must test for."
            )
        )
        corrected_prediction = st.selectbox(
            "The model prediction for this edge case should be:",
            tuple(self.data.testing_data[self.data.target_column].unique()),
        )
        description = "A single edge case."
        return corrected_prediction, description

    def _collect_important_features_feedback(self) -> Tuple[str, int, str]:
        st.write(
            self.__feedback_type_description(
                "you are signalling that a given feature must be in the top N most important features."
            )
        )
        features = self.data.list_features()
        selected_feature = st.selectbox("Choose model feature:", (features))
        top_n_feature = st.slider(
            "The selected feature should be in the top ... features:", min_value=1, max_value=len(features)
        )
        description = "Most important features."
        return selected_feature, top_n_feature, description

    @staticmethod
    def __feedback_type_description(error_description: str) -> str:
        return f"Feedback type description: {error_description}"
