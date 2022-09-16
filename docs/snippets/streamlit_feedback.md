```python
import streamlit as st
from trubrics.feedback_components.streamlit import StreamlitComponent

st_component = StreamlitComponent(model=model, data=data_context)

with st.sidebar:
    st.title("Modify features to test the model...")
    what_if_df = st_component.generate_what_if(TESTING_DATA)

st.title("View model prediction")
raw_prediction = st_component.model.estimator.predict(what_if_df)[0]  # type: ignore
if raw_prediction:
    prediction = '<p style="color:Green;">This passenger would have survived.</p>'
else:
    prediction = '<p style="color:Red;">This passenger would have died.</p>'
st.markdown(prediction, unsafe_allow_html=True)

st.title("Send model feedback")
st_component.feedback(what_if_df=what_if_df, model_prediction=raw_prediction, tracking=True)
```
