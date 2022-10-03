from typing import Any, Optional, Tuple, Union

import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype

from trubrics.context import DataContext, TrubricsModel
from trubrics.exceptions import PandasSchemaError
from trubrics.feedback.dataclass import Feedback
from trubrics.utils.pandas import schema_is_equal


class FeedbackCollector:
    def __init__(self, data: DataContext, model: Any):
        self.trubrics_model = TrubricsModel(data=data, model=model)
        self.model_type = self.trubrics_model.model_type
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
        """Get user feedback and save"""
        feedback_type: str = st.selectbox(
            "Choose feedback type:",
            (
                "Single prediction error",
                "Bias",
                "Important features",
                "Other",
            ),
        )

        if self.what_if_df is None:
            st.text("What-if tool must be set to generate feedback.")
        else:
            metadata = {}
            what_if_input = self.what_if_df.to_dict("records")[0]
            if feedback_type == "Other":
                metadata["description"] = st.text_input(label="", value="Send free text feedback here")
                metadata["what_if_input"] = what_if_input
                metadata["model_prediction"] = self.what_if_prediction

            elif feedback_type == "Single prediction error":
                metadata["corrected_prediction"], metadata["description"] = self._collect_single_edge_case()
                metadata["what_if_input"] = what_if_input

            elif feedback_type == "Important features":
                (
                    metadata["selected_feature"],
                    metadata["top_n_feature"],
                    metadata["description"],
                ) = self._collect_important_features_feedback()

            elif feedback_type == "Bias":
                metadata["description"] = "Feedback on bias."

            else:
                raise NotImplementedError()

            single_test = Feedback(feedback_type=feedback_type, metadata=metadata)
            if st.button("Send feedback"):
                single_test.save_local(path=path, file_name=file_name)
                st.markdown(
                    '<p style="color:Green;">Feedback saved & sent to the Data Science team.</p>',
                    unsafe_allow_html=True,
                )

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
            tuple(self.trubrics_model.data.testing_data[self.trubrics_model.data.target].unique()),
        )
        description = "A single edge case."
        return corrected_prediction, description

    def _collect_important_features_feedback(self) -> Tuple[str, int, str]:
        st.write(
            self.__feedback_type_description(
                "you are signalling that a given feature must be in the top N most important features."
            )
        )
        features = self.trubrics_model.data.features
        selected_feature = st.selectbox("Choose model feature:", (features))
        top_n_feature = st.slider(
            "The selected feature should be in the top ... features:", min_value=1, max_value=len(features)
        )
        description = "Most important features."
        return selected_feature, top_n_feature, description

    @staticmethod
    def __feedback_type_description(error_description: str) -> str:
        return f"Feedback type description: {error_description}"
