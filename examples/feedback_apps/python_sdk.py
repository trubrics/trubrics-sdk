import os

import trubrics

config = trubrics.init(email=os.environ["TRUBRICS_EMAIL"], password=os.environ["TRUBRICS_PASSWORD"])

feedback = trubrics.Feedback(
    component_name="trubrics-example",
    model="your_component_name",
    response={"type": "faces", "score": "🙁", "text": "A comment observation from the user."},
)

trubrics.save(config, feedback)
