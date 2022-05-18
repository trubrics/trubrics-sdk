import joblib
import pandas as pd
import streamlit as st

from trubrics.components.streamlit import feedback, get_streamlit_mapping

# get features from user input and store to df
st.title("Simulate with different features:")
train_df = pd.read_csv("demo/data/preprocessed_train.csv")
target = "Survived"
categoricals = ["Pclass", "Sex", "SubSp", "Parch", "Embarked", "Title"]

df = get_streamlit_mapping(train_df, categoricals, target)

# make predictions
rf_model = joblib.load("demo/models/rf_model.pkl")
raw_prediction = rf_model.predict(df)[0]
if raw_prediction:
    prediction = "survived"
else:
    prediction = "died"
st.title(f"The model prediction is: {prediction}.")

feedback(prediction=prediction, df=df)
