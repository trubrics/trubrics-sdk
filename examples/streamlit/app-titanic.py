import joblib
import pandas as pd
import streamlit as st

from examples.training import titanic_config
from trubrics.context import DataContext
from trubrics.feedback_components.streamlit import StreamlitComponent


# @st.cache
def init_data():
    try:
        TRAINING_DATA = pd.read_csv(titanic_config.LOCAL_TRAIN_FILENAME)
        TESTING_DATA = pd.read_csv(titanic_config.LOCAL_TEST_FILENAME)
        model = joblib.load(titanic_config.LOCAL_MODEL_FILENAME)
    except FileNotFoundError:
        raise FileNotFoundError("To generate these files, run `make train-titanic`")
    # init data context
    data_context = DataContext(
        training_data=TRAINING_DATA,
        testing_data=TESTING_DATA,
        target=titanic_config.TARGET,
        categorical_columns=titanic_config.CATEGORICAL_COLUMNS,
        business_columns=titanic_config.BUSINESS_COLUMNS,
    )
    return data_context, model


data_context, model = init_data()
st_component = StreamlitComponent(data=data_context, model=model)

with st.sidebar:
    st.title("Modify features to test the model...")
    what_if_df = st_component.generate_what_if()

st.title("View model prediction")
raw_prediction = st_component.trubrics_model.model.predict(what_if_df)[0]  # type: ignore
if raw_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
sent = st_component.feedback(what_if_df=what_if_df, model_prediction=raw_prediction, tracking=False)

st.title("View data")
data_view = st.selectbox(label="", options=("View full test set", "View test set errors", "View split by target"))
if data_view == "View full test set":
    st.dataframe(st_component.trubrics_model.data.renamed_testing_data)
elif data_view == "View test set errors":
    st.dataframe(
        st_component.trubrics_model.testing_data_errors.rename(st_component.trubrics_model.data.business_columns)
    )
elif data_view == "View split by target":
    target_split = st.radio(label="", options=("survived", "died"))
    if target_split == "survived":
        st.dataframe(
            st_component.trubrics_model.data.testing_data.loc[lambda x: x[st_component.trubrics_model.data.target] == 0]
        )
    elif target_split == "died":
        st.dataframe(
            st_component.trubrics_model.data.testing_data.loc[lambda x: x[st_component.trubrics_model.data.target] == 1]
        )
    else:
        raise NotImplementedError()

else:
    raise NotImplementedError("The data_view must be one of the selectbox options")
