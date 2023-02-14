import streamlit as st

from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.feedback import (
    collect_feedback_streamlit,
    explore_testing_data,
    generate_what_if_streamlit,
)

_, test_df, model = get_titanic_data_and_model()

data_context = DataContext(
    testing_data=test_df,
    target="Survived",
    categorical_columns=tc.CATEGORICAL_COLUMNS,
    business_columns=tc.BUSINESS_COLUMNS,
)

with st.sidebar:
    st.title("Test the model with different inputs")
    df = generate_what_if_streamlit(data_context=data_context)
wi_prediction = model.predict(df)[0]

st.title("View model prediction")
if wi_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
metadata = {"what_if_data": df.to_dict(), "what_if_prediction": wi_prediction}
collect_feedback_streamlit(
    path="./feedback_issue.json",  # path to save feedback .json to
    tags=["Streamlit"],
    metadata=metadata,
    save_ui=False,  # set to True to save feedback to Trubrics
)

st.title("View data")
explore_testing_data(data_context=data_context, model=model)
