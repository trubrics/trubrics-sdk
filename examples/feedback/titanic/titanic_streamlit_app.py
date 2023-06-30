import streamlit as st

from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.integrations.streamlit import (
    FeedbackCollector,
    generate_what_if_streamlit,
)


@st.cache_resource
def init_trubrics():
    _, test_df, model = get_titanic_data_and_model()

    data_context = DataContext(
        testing_data=test_df,
        target="Survived",
        categorical_columns=tc.CATEGORICAL_COLUMNS,
        business_columns=tc.BUSINESS_COLUMNS,
    )

    return model, data_context


def trubrics_config():
    st.subheader("Input your Trubrics credentials:")
    email = st.text_input(
        label="email", placeholder="email", label_visibility="collapsed", value=st.secrets.get("TRUBRICS_EMAIL", "")
    )

    password = st.text_input(
        label="password",
        placeholder="password",
        label_visibility="collapsed",
        type="password",
        value=st.secrets.get("TRUBRICS_PASSWORD", ""),
    )

    feedback_component = st.text_input(
        label="feedback_component",
        placeholder="Feedback component name",
        label_visibility="collapsed",
    )

    feedback_type = st.radio(
        label="Select the component feedback type:", options=("faces", "thumbs", "textbox"), horizontal=True
    )

    st.write("Don't have an account yet? Create one [here](https://trubrics.streamlit.app/)!")
    return email, password, feedback_component, feedback_type


if "wi_prediction" not in st.session_state:
    st.session_state["wi_prediction"] = None

model, data_context = init_trubrics()
st.title("Titanic Demo App")
with st.sidebar:
    email, password, feedback_component, feedback_type = trubrics_config()
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
            component_name=feedback_component,
            email=email,
            password=password,
        )

        collector.st_feedback(
            feedback_type=feedback_type,
            model="your_model_name",
            open_feedback_label="[Optional] Provide additional feedback",
            metadata=metadata,
        )
else:
    st.warning("Click 'Predict' in the sidebar to generate predictions.")
