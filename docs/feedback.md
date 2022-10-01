# Gather feedback from business users
The trubrics FeedbackCollector enables business users to provide feedback on your models behaviour. The feedback can then be translated into validation points. To achieve this, the trubrics FeedbackCollector integrates with Streamlit to help build python applications on top of your model for the business user to interact with.


To build a trubrics FeedbackCollector, start by initialising a DataContext
--8<-- "docs/snippets/init_datacontext.md"

Then you can create your streamlit app, like the following example:
--8<-- "docs/snippets/streamlit_feedback.md"

A full example can be seen in `examples/feedback_app_titanic.py`, and run with `make streamit-demo`.
