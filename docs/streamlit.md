# FeedbackCollector Streamlit Integration

To get started with [Streamlit](https://streamlit.io/), install the additional dependency:

```console
(venv)$ pip install "trubrics[streamlit]"
```

Then you have two options:

- Run our demo Streamlit app:
    ```console
    (venv)$ trubrics example-app
    ```

    ![logo-gradient](./assets/titanic-feedback-example.png)
    <p align="center"><em>Our demo Streamlit app</em></p>

- OR add this code snippet directly to your streamlit app:
    ```py
    from trubrics.integrations.streamlit import FeedbackCollector

    collector = FeedbackCollector()
    collector.st_feedback(type="issue")  # feedback is saved to a .json file
    ```
