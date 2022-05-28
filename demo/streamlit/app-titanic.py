import joblib
import pandas as pd
import streamlit as st

from demo.streamlit import config
from trubrics.components.streamlit import StreamlitComponent
from trubrics.context import DataContext, ModelContext

# init data
TRAINING_DATA = pd.read_csv(config.LOCAL_TRAIN_FILENAME)
TESTING_DATA = pd.read_csv(config.LOCAL_TRAIN_FILENAME)
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

# Show example of test data
st.title("Example of test data:")
st.dataframe(st_component.get_renamed_test_data())

# make predictions
raw_prediction = st_component.predict(what_if_df)[0]
if raw_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.title("Model prediction:")
st.markdown(prediction, unsafe_allow_html=True)

st_component.feedback(what_if_df=what_if_df)
