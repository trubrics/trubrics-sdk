import streamlit as st

from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.feedback import FeedbackCollector

st.set_page_config(page_title="User Feedback Titanic", page_icon="assets/logo-favicon.png")


# @st.cache
def init_data():
    train_df, test_df, model = get_titanic_data_and_model()

    # init data context
    data_context = DataContext(
        training_data=train_df,
        testing_data=test_df,
        target="Survived",
        categorical_columns=tc.CATEGORICAL_COLUMNS,
        business_columns=tc.BUSINESS_COLUMNS,
    )
    return data_context, model


data_context, model = init_data()
collector = FeedbackCollector(data=data_context, model=model)

with st.sidebar:
    st.title("Modify features to test the model...")
    collector.generate_what_if()

st.title("View model prediction")
if collector.what_if_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
collector.save_feedback(path=".", file_name="feedback.json")

st.title("View data")
data_view = st.selectbox(label="", options=("View full test set", "View test set errors", "View split by target"))
if data_view == "View full test set":
    st.dataframe(collector.trubrics_model.data.renamed_testing_data)
elif data_view == "View test set errors":
    st.dataframe(collector.trubrics_model.testing_data_errors.rename(collector.trubrics_model.data.business_columns))
elif data_view == "View split by target":
    target_split = st.radio(label="", options=("survived", "died"))
    if target_split == "survived":
        st.dataframe(
            collector.trubrics_model.data.testing_data.loc[lambda x: x[collector.trubrics_model.data.target] == 0]
        )
    elif target_split == "died":
        st.dataframe(
            collector.trubrics_model.data.testing_data.loc[lambda x: x[collector.trubrics_model.data.target] == 1]
        )
    else:
        raise NotImplementedError()

else:
    raise NotImplementedError("The data_view must be one of the selectbox options")
