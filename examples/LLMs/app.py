import os

import dotenv
import openai
import streamlit as st

dotenv.load_dotenv(".env")

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
        "Enter your OpenAI API Key", type="password", value=os.environ["TRUBRICS_OPENAI_API_KEY"]
    )

prompt = st.text_area(label="Prompt", label_visibility="collapsed", placeholder="What would you like to know?")
button = st.button(f"Ask {model}")
if button:
    st.session_state["response"] = openai.Completion.create(model=model, prompt=prompt, temperature=0.5, max_tokens=200)

if st.session_state["response"]:
    response = st.session_state["response"]
    response_text = response.choices[0].text.replace("\n", "")
    st.markdown(f"#### :violet[{response_text}]")

    from trubrics.integrations.streamlit import FeedbackCollector

    collector = FeedbackCollector(component_name="llm-demo", trubrics_platform_auth="single_user", model=response.model)

    feedback = collector.st_feedback(
        feedback_type="thumbs",
        open_feedback_label="Optionally please provide more detailed feedback",
        metadata={"model_type": response.object},
        model_input=prompt,
        model_output=response_text,
    )

    if feedback:
        st.markdown(":green[View your feedback here: https://trubrics-streamlit.com]")
        st.session_state["response"] = ""
