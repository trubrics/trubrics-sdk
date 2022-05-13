import joblib
import pandas as pd
import streamlit as st

from trubrics.components.streamlit import feedback

# get features from user input and store to df
st.title("Simulate with different features:")
df = pd.DataFrame()
df["Pclass"] = [st.slider("Ticket Class", min_value=1, max_value=3, value=2)]
df["Sex"] = [st.selectbox("Sex", ("male", "female"))]
df["Age"] = [st.number_input("Age", min_value=0, max_value=100, value=28)]
df["SibSp"] = [st.slider("SibSp", min_value=0, max_value=8, value=2)]
df["Parch"] = [st.slider("Parch", min_value=0, max_value=9, value=2)]
df["Fare"] = [st.number_input("Fare", min_value=0, max_value=1000, value=2)]
df["Embarked"] = [st.selectbox("Embarked", ("Q", "S", "C"))]
df["Title"] = [st.selectbox("Title", ("Mr", "Mrs", "Miss", "Master", "Ms", "Col", "Rev", "Dr", "Dona"))]

# make predictions
rf_model = joblib.load("demo/models/rf_model.pkl")
raw_prediction = rf_model.predict(df)[0]
if raw_prediction:
    prediction = "survived"
else:
    prediction = "died"
st.title(f"The model prediction is: {prediction}.")

feedback(prediction=prediction, df=df)
