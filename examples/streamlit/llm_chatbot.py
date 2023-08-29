import uuid

import openai
import streamlit as st
from trubrics_utils import trubrics_config, trubrics_successful_feedback

from trubrics.integrations.streamlit import FeedbackCollector

with st.sidebar:
    email, password = trubrics_config()


@st.cache_data
def init_trubrics(email, password):
    collector = FeedbackCollector(email=email, password=password, project="default")
    return collector


collector = init_trubrics(email, password)


st.title("💬 Trubrics - Chat with user feedback")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
if "prompt_ids" not in st.session_state:
    st.session_state["prompt_ids"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

model = "gpt-3.5-turbo"

openai_api_key = st.secrets.get("OPENAI_API_KEY")
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model=model, messages=st.session_state.messages)
    msg = response.choices[0].message
    logged_prompt = collector.log_prompt(
        config_model={"model": model},
        prompt=prompt,
        generation=msg["content"],
        session_id=st.session_state.session_id,
        tags=["llm_chatbot.py"],
    )
    st.session_state.prompt_ids.append(logged_prompt.id)
    st.session_state.messages.append(msg)

feedback = None
for n, msg in enumerate(st.session_state.messages):
    st.chat_message(msg["role"]).write(msg["content"])

    if msg["role"] == "assistant" and msg["content"] != "How can I help you?":
        if email and password:
            feedback = collector.st_feedback(
                component="default",
                feedback_type="thumbs",
                model=model,
                prompt_id=st.session_state.prompt_ids[int(n / 2) - 1],
                open_feedback_label="[Optional] Provide additional feedback",
                align="flex-end",
                single_submit=True,
                key=f"feedback_{int(n/2)}",
                tags=["llm_chatbot.py"],
            )

        else:
            st.warning("To save some feedback to Trubrics, add your account details in the sidebar.")

if feedback:
    trubrics_successful_feedback(feedback)
