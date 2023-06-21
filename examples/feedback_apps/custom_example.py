import streamlit as st

from trubrics.integrations.streamlit import FeedbackCollector

collector = FeedbackCollector(component_name="default", email="jeff", password="...")

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
            model="model a",
            response={  # type: ignore
                "type": "custom",
                "score": st.session_state["test 1"],
                "text": st.session_state["test 2"],
            },
            metadata={
                "test 3": st.session_state["test 3"],
                "test 4": st.session_state["test 4"],
            },
        )
        st.write(feedback)

st.session_state
