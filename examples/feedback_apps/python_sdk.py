import os

import trubrics

config = trubrics.init(email=os.environ["TRUBRICS_EMAIL"], password=os.environ["TRUBRICS_PASSWORD"])

feedback = trubrics.Feedback(
    component_name="default",
    model="default_model",
    response={"type": "thumbs", "score": "👎", "text": "A comment / textual feedback from the user."},
)

trubrics.save(config, feedback)
