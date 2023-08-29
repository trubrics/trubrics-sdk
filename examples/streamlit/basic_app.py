import streamlit as st

from trubrics.integrations.streamlit import FeedbackCollector

if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = None

collector = FeedbackCollector(email=st.secrets.TRUBRICS_EMAIL, password=st.secrets.TRUBRICS_PASSWORD, project="default")

if st.button("Predict"):
    st.session_state.logged_prompt = collector.log_prompt(
        config_model={"model": "gpt-3.5-turbo"},
        prompt="Tell me a joke",
        generation="Why did the chicken cross the road? To get to the other side.",
    )

if st.session_state.logged_prompt:
    st.write("A model generation...")
    user_feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        model=st.session_state.logged_prompt.config_model.model,
        prompt_id=st.session_state.logged_prompt.id,
        align="flex-start",
        single_submit=False,
    )
