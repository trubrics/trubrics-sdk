import streamlit as st

from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector()

st.text_input("test 1", key="test 1")
st.text_input("test 2", key="test 2")
st.text_input("test 3", key="test 3")
st.text_input("test 4", key="test 4")

if (
    st.session_state.get("test 1")
    and st.session_state.get("test 2")
    and st.session_state.get("test 3")
    and st.session_state.get("test 4")
):
    button = st.button(label="submit")

    if button:
        feedback = collector.st_feedback(
            "custom",
            user_response={
                "test 1": st.session_state["test 1"],
                "test 2": st.session_state["test 2"],
                "test 3": st.session_state["test 3"],
                "test 4": st.session_state["test 4"],
            },
            path="./feedback.json",
        )
        st.write(feedback.dict() if feedback else None)

st.session_state
