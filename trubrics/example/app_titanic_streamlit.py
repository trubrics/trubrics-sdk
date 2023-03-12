import streamlit as st
import typer

from trubrics.context import DataContext
from trubrics.example import get_titanic_data_and_model
from trubrics.example import titanic_config as tc
from trubrics.feedback import (
    FeedbackCollector,
    explore_testing_data,
    generate_what_if_streamlit,
)

cli = typer.Typer()


@cli.command()
def main(save_ui: bool = False):
    _, test_df, model = get_titanic_data_and_model()

    data_context = DataContext(
        testing_data=test_df,
        target="Survived",
        categorical_columns=tc.CATEGORICAL_COLUMNS,
        business_columns=tc.BUSINESS_COLUMNS,
    )

    with st.sidebar:
        st.title("Test the model with different inputs")
        df = generate_what_if_streamlit(data_context=data_context)
    wi_prediction = model.predict(df)[0]

    metadata = {"what_if_data": df.to_dict(), "what_if_prediction": wi_prediction}
    collector = FeedbackCollector(
        data_context=data_context,
        model_name="my_model",
        model_version="v0.0.1",
        tags=["Streamlit"],
        save_ui=save_ui,  # set to True to save feedback to Trubrics
    )

    st.title("View model prediction")
    if wi_prediction:
        prediction = '<p style="color:Green;">This passenger would have survived.</p>'
    else:
        prediction = '<p style="color:Red;">This passenger would have died.</p>'
    st.markdown(prediction, unsafe_allow_html=True)
    collector.st_feedback(type="thumbs", metadata=metadata)

    st.title("Report an issue")
    collector.st_feedback(type="issue", metadata=metadata)

    st.title("View data")
    explore_testing_data(data_context=data_context, model=model)
    collector.st_feedback(type="faces")


if __name__ == "__main__":
    cli(standalone_mode=False)
