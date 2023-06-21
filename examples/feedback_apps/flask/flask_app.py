import os

from flask import Flask, flash, redirect, render_template, request

from trubrics.feedback.dataclass import Feedback

app = Flask(__name__)
app.config["SECRET_KEY"] = "Trubrics Demo Flask App"

project_name = os.environ["TRUBRICS_PROJECT_NAME"]


@app.route("/", methods=["GET"])
def feedback_form():
    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    faces_feedback = request.form.get("faces")
    thumbs_feedback = request.form.get("thumbs")
    user_response = None
    if faces_feedback:
        feedback_type = "faces"
        user_response = {f"User satisfaction: {feedback_type}": faces_feedback}
    elif thumbs_feedback:
        feedback_type = "thumbs"
        user_response = {f"User satisfaction: {feedback_type}": thumbs_feedback}
    else:
        raise ValueError()

    if feedback_type and user_response:
        trubrics_feedback = Feedback(
            feedback_type=feedback_type,
            user_response=user_response,  # type: ignore
            data=None,
            tags=["Flask"],
        )
        trubrics_feedback.save_ui(email=None, password=None)
        flash(f"{feedback_type} feedback saved to the Trubrics platform.")
    return redirect("/")


@app.route("/submit_feedback_text", methods=["POST"])
def submit_feedback_text():
    feedback = request.form.get("text")
    trubrics_feedback = Feedback(
        feedback_type="issue",
        user_response={"text": feedback or ""},
        data=None,
        tags=["Flask"],
    )
    trubrics_feedback.save_ui(email=None, password=None)
    flash("Text feedback saved to the Trubrics platform.")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
