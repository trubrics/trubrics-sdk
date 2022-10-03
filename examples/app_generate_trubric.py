import joblib
import pandas as pd
import streamlit as st
from sklearn.metrics import SCORERS

from trubrics.context import DataContext
from trubrics.validations import ModelValidator, Trubric
from trubrics.validations.run import TrubricRun, run_trubric


def expand_docstring(func):
    expander = st.expander("See docstring")
    stripped_docstring = "\n".join(" ".join(line.split()) for line in func.__doc__.split("\n"))
    expander.text(stripped_docstring)


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
            perf_thresh = st.checkbox("validate_performance_against_threshold")
        with col2:
            metric = st.selectbox("1. Metric", SCORERS)
        with col3:
            threshold = st.number_input("1. Threshold", min_value=-1.0, max_value=1.0, value=0.2, step=0.1)
        expand_docstring(model_validator.validate_performance_against_threshold)
        if perf_thresh:
            perf_vs_thresh = model_validator.validate_performance_against_threshold(
                metric=metric,
                threshold=threshold,
            )
            validations.append(perf_vs_thresh)
            st.write(perf_vs_thresh.dict())

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            perf_dum = st.checkbox("validate_test_performance_against_dummy")
        with col2:
            metric = st.selectbox("2. Metric", SCORERS)
        with col3:
            strategy = st.selectbox("2. Strategy", ["most_frequent", "prior", "stratified", "uniform", "constant"])
            if strategy == "constant":
                cst_value = st.text_input("Enter constant value")
                if cst_value.isnumeric():
                    cst_value = int(cst_value)
                dummy_kwarg = {"metric": metric, "strategy": strategy, "dummy_kwargs": {"constant": cst_value}}
            else:
                dummy_kwarg = {"metric": metric, "strategy": strategy}
        expand_docstring(model_validator.validate_test_performance_against_dummy)
        if perf_dum:
            perf_vs_dummy = model_validator.validate_test_performance_against_dummy(**dummy_kwarg)
            validations.append(perf_vs_dummy)
            st.write(perf_vs_dummy.dict())

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            perf_train = st.checkbox("validate_performance_between_train_and_test")
        with col2:
            metric = st.selectbox("3. Metric", SCORERS)
        with col3:
            threshold = st.number_input("3. Threshold", min_value=-1.0, max_value=1.0, value=0.2, step=0.1)
        expand_docstring(model_validator.validate_performance_between_train_and_test)
        if perf_train:
            perf_vs_train = model_validator.validate_performance_between_train_and_test(
                metric=metric, threshold=threshold
            )
            validations.append(perf_vs_train)
            st.write(perf_vs_train.dict())

        col1, col2, col3 = st.columns([2, 1.4, 1])
        with col1:
            inf_time = st.checkbox("validate_inference_time")
        with col2:
            threshold = st.number_input("4. Threshold (s)", min_value=0.0, max_value=100.0, value=0.1, step=0.1)
        with col3:
            n_executions = st.number_input("4. n_executions", min_value=1, max_value=1000, value=100, step=50)
        expand_docstring(model_validator.validate_inference_time)
        if inf_time:
            inference_time = model_validator.validate_inference_time(threshold=threshold, n_executions=n_executions)
            validations.append(inference_time)
            st.write(inference_time.dict())

        with tab2:
            tc = Trubric(data_context_name="data", data_context_version=0.1, validations=validations)

            path = st.text_input("Filepath to save trubric to:")
            if st.button("Save trubric locally"):
                tc.save_local(path)
                msg = f'<p style="color:Green;">Trubric saved to {path}/my_trubric.json!</p>'
                st.markdown(msg, unsafe_allow_html=True)

            if st.button("Run saved trubric"):
                trubric = Trubric.parse_file(f"{path}/my_trubric.json")

                run_context = TrubricRun(
                    data_context=data_context,  # type: ignore
                    model=model,  # type: ignore
                    trubric=trubric,
                )

                all_validation_results = run_trubric(run_context)

                for validation_result in all_validation_results:
                    message_start = f"{validation_result.validation_type} - {validation_result.severity.upper()}"
                    completed_dots = (100 - len(message_start)) * "."
                    if validation_result.outcome == "pass":
                        msg = f'<p style="color:Green;">{message_start + completed_dots + "PASSED"}</p>'
                    else:
                        msg = f'<p style="color:Red;">{message_start + completed_dots + "FAILED"}</p>'
                    st.markdown(msg, unsafe_allow_html=True)
