import joblib
import pandas as pd
import streamlit as st
from sklearn.metrics import SCORERS

from trubrics.context import DataContext, TrubricContext
from trubrics.validations import ModelValidator
from trubrics.validations.run import run_trubric


def get_spaces(number_rows=2):
    _ = [st.write("") for x in range(number_rows)]


st.set_page_config(layout="wide")

st.sidebar.title("Initialise a ModelValidator")
test_data = st.sidebar.file_uploader("Upload a test dataset")
train_data = st.sidebar.file_uploader("Upload a train dataset")
if test_data and train_data:
    test_df = pd.read_csv(test_data)
    train_df = pd.read_csv(train_data)
    st.sidebar.write("Preview of uploaded data:", test_df.head())
    target = st.sidebar.selectbox("Select the target variable from the uploaded test dataset:", test_df.columns)
    data_context = DataContext(
        testing_data=test_df,
        training_data=train_df,
        target=target,
    )

model_ = st.sidebar.file_uploader("Upload a model")
if model_ is not None:
    model = joblib.load(model_)

if model_ and test_data and train_data:
    model_validator = ModelValidator(data=data_context, model=model)  # type: ignore

    tab1, tab2 = st.tabs(["Select Model Validations", "Save Trubric"])

    with tab1:
        validations = []

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            get_spaces(number_rows=3)
            perf_thresh = st.checkbox("validate_performance_against_threshold")
        with col2:
            metric = st.selectbox("1. Metric", SCORERS)
        with col3:
            threshold = st.number_input("1. Threshold", min_value=-1.0, max_value=1.0, value=0.2, step=0.1)
        if perf_thresh:
            perf_vs_thresh = model_validator.validate_performance_against_threshold(
                metric=metric,
                threshold=threshold,
            )
            validations.append(perf_vs_thresh)
            st.write(perf_vs_thresh.dict())

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            get_spaces(number_rows=3)
            perf_dum = st.checkbox("validate_performance_against_dummy")
        with col2:
            metric = st.selectbox("2. Metric", SCORERS)
        with col3:
            strategy = st.selectbox("2. Strategy", ["most_frequent", "prior", "stratified", "uniform", "constant"])
        if perf_dum:
            perf_vs_dummy = model_validator.validate_performance_against_dummy(metric="accuracy", strategy="stratified")
            validations.append(perf_vs_dummy)
            st.write(perf_vs_dummy.dict())

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            get_spaces(number_rows=3)
            perf_train = st.checkbox("validate_performance_between_train_and_test")
        with col2:
            metric = st.selectbox("3. Metric", SCORERS)
        with col3:
            strategy = st.number_input("3. Threshold", min_value=-1.0, max_value=1.0, value=0.2, step=0.1)
        if perf_train:
            perf_vs_train = model_validator.validate_performance_between_train_and_test(metric="recall", threshold=0.3)
            validations.append(perf_vs_train)
            st.write(perf_vs_train.dict())

        with tab2:
            tc = TrubricContext(data_context_name="data", data_context_version=0.1, validations=validations)

            path = st.text_input("Filepath to save trubric to:")
            if st.button("Save trubric locally"):
                tc.save_local(path)
                msg = f'<p style="color:Green;">Trubric saved to {path}/my_trubric.json!</p>'
                st.markdown(msg, unsafe_allow_html=True)

            if st.button("Run saved trubric"):
                trubric = TrubricContext.parse_file(f"{path}/my_trubric.json")

                all_validation_results = run_trubric(
                    data_context=data_context,  # type: ignore
                    model=model,  # type: ignore
                    trubric=trubric,
                )

                for validation_result in all_validation_results:
                    message_start = f"{validation_result.validation_type} - {validation_result.severity.upper()}"
                    completed_dots = (100 - len(message_start)) * "."
                    if validation_result.outcome == "pass":
                        msg = f'<p style="color:Green;">{message_start + completed_dots + "PASSED"}</p>'
                    else:
                        msg = f'<p style="color:Red;">{message_start + completed_dots + "FAILED"}</p>'
                    st.markdown(msg, unsafe_allow_html=True)
