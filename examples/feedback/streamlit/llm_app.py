import openai
import streamlit as st
from trubrics_utils import trubrics_config, trubrics_successful_feedback

if "response" not in st.session_state:
    st.session_state["response"] = ""


st.title("LLM User Feedback with Trubrics")

with st.sidebar:
    email, password = trubrics_config()

models = ("text-davinci-003", "text-davinci-002")
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
    st.session_state["response"] = openai.Completion.create(model=model, prompt=prompt, temperature=0.5, max_tokens=200)

if st.session_state["response"]:
    response_text = st.session_state["response"].choices[0].text.replace("\n", "")
    st.markdown(f"#### :violet[{response_text}]")

    from trubrics.integrations.streamlit import FeedbackCollector

    if email and password:
        collector = FeedbackCollector(
            component_name="default",
            email=email,
            password=password,
        )

        feedback = collector.st_feedback(
            feedback_type="thumbs",
            model=model,
            open_feedback_label="[Optional] Provide additional feedback",
            metadata={"response": st.session_state["response"], "prompt": prompt},
            align="flex-start",
            single_submit=False,
        )

        if feedback:
            trubrics_successful_feedback(feedback)

    else:
        st.warning("To save some feedback to Trubrics, add your account details in the sidebar.")
