import joblib
import pandas as pd
import streamlit as st

from examples.streamlit import config
from trubrics.components.streamlit import StreamlitComponent
from trubrics.context import DataContext, ModelContext

# init data
TRAINING_DATA = pd.read_csv(config.LOCAL_TRAIN_FILENAME)
TESTING_DATA = pd.read_csv(config.LOCAL_TEST_FILENAME)
data_context = DataContext(
    training_data=TRAINING_DATA,
    testing_data=TESTING_DATA,
    target_column=config.TARGET,
    categorical_columns=config.CATEGORICAL_COLUMNS,
    business_columns=config.BUSINESS_COLUMNS,
)
# init model
RF_MODEL = joblib.load(config.LOCAL_MODEL_FILENAME)
model_context = ModelContext(estimator=RF_MODEL, evaluation_function=lambda x, y: x.min() - y.min())

# create streamlit component
st_component = StreamlitComponent(model=model_context, data=data_context)

with st.sidebar:
    what_if_df = st_component.generate_what_if(TESTING_DATA)


st.title("View model prediction")


def get_what_if_prediction(what_if_df):
    raw_prediction = st_component.predict(what_if_df)[0]
    if raw_prediction:
        prediction = '<p style="color:Green;">This passenger would have survived.</p>'
    else:
        prediction = '<p style="color:Red;">This passenger would have died.</p>'
    return prediction


prediction = get_what_if_prediction(what_if_df)
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
st_component.feedback(what_if_df=what_if_df)

st.title("View data")
data_view = st.selectbox(label="", options=("View full test set", "View test set errors", "View split by target"))
if data_view == "View full test set":
    st.dataframe(st_component.get_renamed_test_data())
elif data_view == "View test set errors":
    st.dataframe(st_component.explore_test_set_errors(business_columns=True))
elif data_view == "View split by target":
    target_split = st.radio(label="", options=("survived", "died"))
    if target_split == "survived":
        st.dataframe(st_component.data.testing_data.loc[lambda x: x[st_component.data.target_column] == 0])
    elif target_split == "died":
        st.dataframe(st_component.data.testing_data.loc[lambda x: x[st_component.data.target_column] == 1])
    else:
        raise NotImplementedError()

else:
    raise NotImplementedError("The data_view must be one of the selectbox options")
