import openai
import streamlit as st
from trubrics_utils import trubrics_config, trubrics_successful_feedback

from trubrics.integrations.streamlit import FeedbackCollector

if "response" not in st.session_state:
    st.session_state.response = ""
if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = ""

st.title("LLM User Feedback with Trubrics")

with st.sidebar:
    email, password = trubrics_config()

if email and password:
    collector = FeedbackCollector(
        project="default",
        email=email,
        password=password,
    )
else:
    st.warning("To save some feedback to Trubrics, add your account details in the sidebar.")

models = ("gpt-3.5-turbo",)
model = st.selectbox(
    "Choose your GPT-3.5 LLM",
    models,
    help="Consult https://platform.openai.com/docs/models/gpt-3-5 for model info.",
)

openai.api_key = st.secrets.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OpenAI key is missing. Set OPENAI_API_KEY in st.secrets")

prompt = st.text_area(label="Prompt", label_visibility="collapsed", placeholder="What would you like to know?")
button = st.button(f"Ask {model}")

if button:
    response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
    response_text = response.choices[0].message["content"]
    st.session_state.logged_prompt = collector.log_prompt(
        model_config={"model": model}, prompt=prompt, generation=response_text, tags=["llm_app.py"]
    )
    st.session_state.response = response_text

if st.session_state.response:
    st.markdown(f"#### :violet[{st.session_state.response}]")

    feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        prompt_id=st.session_state.logged_prompt.id,
        model=model,
        align="flex-start",
        single_submit=False,
        tags=["llm_app.py"],
    )

    if feedback:
        trubrics_successful_feedback(feedback)
