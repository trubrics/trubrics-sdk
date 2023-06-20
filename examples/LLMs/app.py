import openai
import streamlit as st

if "response" not in st.session_state:
    st.session_state["response"] = ""


st.title("LLM User Feedback with Trubrics")

col1, col2 = st.columns(2)
with col1:
    models = ("text-davinci-003", "text-davinci-002")
    model = st.selectbox(
        "Choose your GPT-3.5 LLM",
        models,
        help="Consult https://platform.openai.com/docs/models/gpt-3-5 for model info.",
    )
with col2:
    openai.api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        value=st.secrets.get("OPENAI_API_KEY"),
        help="We are not storing your API key.",
    )

prompt = st.text_area(label="Prompt", label_visibility="collapsed", placeholder="What would you like to know?")
button = st.button(f"Ask {model}")

if button:
    st.session_state["response"] = openai.Completion.create(model=model, prompt=prompt, temperature=0.5, max_tokens=200)

if st.session_state["response"]:
    response_text = st.session_state["response"].choices[0].text.replace("\n", "")
    st.markdown(f"#### :violet[{response_text}]")

    from trubrics import FeedbackCollector

    collector = FeedbackCollector(
        component_name="thumbs-example",
        email=st.secrets["TRUBRICS_EMAIL"],
        password=st.secrets["TRUBRICS_PASSWORD"],
    )

    feedback = collector.st_feedback(
        feedback_type="thumbs",
        model=model,
        open_feedback_label="Please provide a comment",
        metadata={"response": st.session_state["response"], "prompt": prompt},
    )

    if feedback:
        st.markdown(":green[View your feedback here: https://trubrics-streamlit.com]")
