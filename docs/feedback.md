# Gather feedback from business users
Trubrics feedback components allows data science teams to "close the loop" and speed up model iterations with
business users. Giving teams the possibility to quickly build web applications in python to collect feedback 
will also help to build validations for a project. [Streamlit](https://streamlit.io/) is the python web framework that
is currently supported.

Building a feedback component starts with initialising a DataContext:
--8<-- "docs/snippets/init_datacontext.md"

Then you can create your streamlit app with something like:
--8<-- "docs/snippets/streamlit_feedback.md"

A full example can be seen in `examples/app-titanic.py`, and run with `make streamit-demo`.
