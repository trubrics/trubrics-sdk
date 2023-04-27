import openai
import streamlit as st

from trubrics.cli.main import init
from trubrics.integrations.streamlit import FeedbackCollector


@st.cache(allow_output_mutation=True)
def init_trubrics():
    with st.spinner("Connecting to the Trubrics platform..."):
        init(project_name="LLM demo")
    return FeedbackCollector(trubrics_platform_auth="single_user")


if "response" not in st.session_state:
    st.session_state["response"] = ""

collector = init_trubrics()

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
    openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")

prompt = st.text_area(label="Prompt", label_visibility="collapsed", placeholder="What would you like to know?")
button = st.button(f"Ask {model}")
if button:
    st.session_state["response"] = openai.Completion.create(model=model, prompt=prompt, temperature=0.5, max_tokens=200)

if st.session_state["response"]:
    response = st.session_state["response"]
    response_text = response.choices[0].text.replace("\n", "")
    st.markdown(f"#### :violet[{response_text}]")
    collector.model = response.model
    feedback = collector.st_feedback(
        "thumbs",
        open_feedback_label="Optionally provide some detail on how the LLM responded:",
        metadata={"model_type": response.object, "prompt": prompt, "model_response": response.choices[0].text},
        tags=["llm-demo"],
    )
    feedback.dict() if feedback else None
