import streamlit as st
from trubrics_utils import trubrics_config, trubrics_successful_feedback

from examples.streamlit.titanic.experiment import generate_what_if_streamlit
from examples.streamlit.titanic.training import get_titanic_data_and_model
from trubrics.integrations.streamlit import FeedbackCollector

st.error("Titanic app is currently under maintenance.")
st.stop()


@st.cache_resource
def init_trubrics():
    _, test_df, model = get_titanic_data_and_model()

    data_context = None

    return model, data_context


if "wi_prediction" not in st.session_state:
    st.session_state["wi_prediction"] = None

model, data_context = init_trubrics()
st.title("Titanic Demo App")
with st.sidebar:
    email, password, feedback_component, feedback_type = trubrics_config(default_component=False)
    with st.form("form"):
        st.subheader("Test the model with different inputs")
        df = generate_what_if_streamlit(data_context=data_context)
        submit = st.form_submit_button("Predict")

metadata = None
if submit:
    st.session_state["wi_prediction"] = model.predict(df)[0]
st.markdown("")

if st.session_state["wi_prediction"] is not None:
    metadata = {"data": df.to_dict(), "prediction": st.session_state["wi_prediction"]}

    prediction = (
        "## :orange["
        + str(st.session_state["wi_prediction"])
        + f"{' (survived)' if st.session_state['wi_prediction'] else  ' (did not survive)'}]"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## :orange[Model prediction:]")
    with col2:
        st.markdown(prediction, unsafe_allow_html=True)
    if email and password:
        collector = FeedbackCollector(
            project="default",
            email=email,
            password=password,
        )

        feedback = collector.st_feedback(
            component=feedback_component,
            feedback_type=feedback_type,
            model="your_model_name",
            open_feedback_label="[Optional] Provide additional feedback",
            metadata=metadata,
            align="flex-start",
            single_submit=False,
        )
        if feedback:
            trubrics_successful_feedback(feedback)
else:
    st.warning("Click 'Predict' in the sidebar to generate predictions.")
