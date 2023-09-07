import uuid

import openai
import streamlit as st
from trubrics_utils import trubrics_config, trubrics_successful_feedback

from trubrics.integrations.streamlit import FeedbackCollector

st.title("💬 Trubrics - Chat with user feedback")

with st.sidebar:
    email, password = trubrics_config()

if not email or not password:
    st.info(
        "To chat with an LLM and save your feedback to Trubrics, add your email and password in the sidebar."
        " Don't have an account yet? Create one for free [here](https://trubrics.streamlit.app/)!"
    )
    st.stop()


@st.cache_data
def init_trubrics(email, password):
    try:
        collector = FeedbackCollector(email=email, password=password, project="default")
        return collector
    except Exception:
        st.error(f"Error authenticating '{email}'. Please try again.")
        st.stop()


collector = init_trubrics(email, password)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
if "prompt_ids" not in st.session_state:
    st.session_state["prompt_ids"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

model = st.secrets.get("OPENAI_API_MODEL") or "gpt-3.5-turbo"

openai_api_key = st.secrets.get("OPENAI_API_KEY")

messages = st.session_state.messages
feedback_kwargs = {
    "component": "default",
    "feedback_type": "thumbs",
    "open_feedback_label": "[Optional] Provide additional feedback",
    "model": model,
    "tags": ["llm_chatbot.py"],
}

for n, msg in enumerate(messages):
    st.chat_message(msg["role"]).write(msg["content"])

    if msg["role"] == "assistant" and n > 1:
        if email and password:
            feedback_key = f"feedback_{int(n/2)}"

            if feedback_key not in st.session_state:
                st.session_state[feedback_key] = None

            disable_with_score = st.session_state[feedback_key].get("score") if st.session_state[feedback_key] else None
            feedback = collector.st_feedback(
                **feedback_kwargs,
                key=feedback_key,
                disable_with_score=disable_with_score,
                prompt_id=st.session_state.prompt_ids[int(n / 2) - 1],
            )
            if feedback:
                trubrics_successful_feedback(feedback)


if prompt := st.chat_input():
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(model=model, messages=messages)
    generation = response.choices[0].message.content

    with st.chat_message("assistant"):
        logged_prompt = collector.log_prompt(
            config_model={"model": model},
            prompt=prompt,
            generation=generation,
            session_id=st.session_state.session_id,
            tags=["llm_chatbot.py"],
        )
        st.session_state.prompt_ids.append(logged_prompt.id)
        messages.append({"role": "assistant", "content": generation})
        st.write(generation)

    feedback = collector.st_feedback(
        **feedback_kwargs,
        key=f"feedback_{int(len(messages)/2)}",
        prompt_id=st.session_state.prompt_ids[int(len(messages) / 2) - 1],
    )
    if feedback:
        trubrics_successful_feedback(feedback)
