import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request

import trubrics

app = Flask(__name__)
app.config["SECRET_KEY"] = "Trubrics Demo Flask App"


@app.route("/", methods=["GET"])
def feedback_form():
    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    faces_feedback = request.form.get("faces")
    thumbs_feedback = request.form.get("thumbs")
    text_feedback = request.form.get("text")
    user_response = None
    if faces_feedback:
        feedback_type = "faces"
        # user_response = faces_feedback
        flash(f"feedback_type={feedback_type} is not valid for `default` component.")
    elif thumbs_feedback:
        feedback_type = "thumbs"
        user_response = thumbs_feedback
    elif text_feedback:
        feedback_type = "textbox"
        # user_response = text_feedback
        flash(f"feedback_type={feedback_type} is not valid for `default` component.")
    else:
        raise ValueError()

    if feedback_type and user_response:
        config = trubrics.init(email=os.environ["TRUBRICS_EMAIL"], password=os.environ["TRUBRICS_PASSWORD"])

        feedback = trubrics.collect(
            component_name="default",
            model="your_model_name",
            response={
                "type": feedback_type,
                "score": user_response,
                "text": "A comment / textual feedback from the user.",
            },
            created_on=datetime.now(),
        )
        trubrics.save(config, feedback)
        flash(f"{feedback_type} feedback saved to Trubrics.")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
