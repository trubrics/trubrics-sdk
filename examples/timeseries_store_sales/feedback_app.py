import joblib
import pandas as pd
import streamlit as st

from trubrics.context import DataContext
from trubrics.feedback import FeedbackCollector

path = "examples/timeseries_store_sales/store-sales-time-series-forecasting/"

test_df = pd.read_csv(path + "sample_x_test.csv")
model = joblib.load(path + "xgb.joblib")

data_context = DataContext(
    testing_data=test_df,
    target="sales",
    categorical_columns=["family", "city", "state", "type"],
)

collector = FeedbackCollector(data=data_context, model=model)

with st.sidebar:
    st.title("Modify features to test the model...")
    collector.generate_what_if()

st.title("View model prediction")
st.text(collector.what_if_prediction)

st.title("Send model feedback")
collector.save_feedback(path=".", file_name="feedback.json")
