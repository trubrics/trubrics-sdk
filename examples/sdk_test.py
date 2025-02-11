import os
from trubrics import Trubrics

trubrics = Trubrics(api_key=os.environ["TRUBRICS_API_KEY"])
trubrics.track(event="Sign up", user_id="user_id")

trubrics.track_llm(
    user_id="user_id",
    prompt="What is Trubrics?",
    assistant_id="gpt4o",
    generation="Trubrics is a product analytics platform for AI applications.",
    latency=2,
)

trubrics.close()