from typing import Optional

import streamlit as st
import typer

from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.integrations.streamlit import (
    FeedbackCollector,
    generate_what_if_streamlit,
)

cli = typer.Typer()


@st.cache(allow_output_mutation=True)
def init_trubrics(trubrics_platform_auth):
    _, test_df, model = get_titanic_data_and_model()

    data_context = DataContext(
        testing_data=test_df,
        target="Survived",
        categorical_columns=tc.CATEGORICAL_COLUMNS,
        business_columns=tc.BUSINESS_COLUMNS,
    )

    collector = FeedbackCollector(
        data_context=data_context,
        model_name="my_model",
        model_version="v0.0.1",
        trubrics_platform_auth=trubrics_platform_auth,
    )
    return model, data_context, collector


@cli.command()
def main(trubrics_platform_auth: Optional[str] = None):
    model, data_context, collector = init_trubrics(trubrics_platform_auth)

    st.title("Titanic Demo App")

    with st.sidebar:
        if trubrics_platform_auth == "multiple_users":
            st.title("Authentication")
            collector.st_trubrics_auth()
        st.title("Test the model with different inputs")
        df = generate_what_if_streamlit(data_context=data_context)
    wi_prediction = model.predict(df)[0]

    metadata = {"data": df.to_dict(), "prediction": wi_prediction}

    prediction = "## " + str(wi_prediction) + f"{' (survived)' if wi_prediction else  ' (did not survive)'}"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Model prediction:")
    with col2:
        st.markdown(prediction, unsafe_allow_html=True)

    st.markdown("## 3 types of feedback:")

    st.markdown('##### 1 - "Does this prediction look correct?"')
    collector.st_feedback(type="thumbs", metadata=metadata, path="./thumbs_feedback.json")
    st.markdown("***")

    st.markdown('##### 2 - "How satisfied are you with this prediction?"')
    collector.st_feedback(type="faces", metadata=metadata, path="./thumbs_faces.json")
    st.markdown("***")

    st.markdown('##### 3 - "Provide your feedback!"')
    collector.st_feedback(type="issue", metadata=metadata, path="./thumbs_issue.json")


if __name__ == "__main__":
    cli(standalone_mode=False)
