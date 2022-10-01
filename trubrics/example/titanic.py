import pandas as pd
import pkg_resources  # type: ignore
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

import trubrics.example.titanic_config as tc


def read_test_data():
    stream = pkg_resources.resource_stream(__name__, "titanic_data.csv")
    return pd.read_csv(stream)


def get_titanic_data_and_model():
    df = read_test_data()
    preprocessed_train = df.pipe(preprocess)

    numerical_cols = [col for col in preprocessed_train.columns if col not in tc.CATEGORICAL_COLUMNS + [tc.TARGET]]

    training_pipeline = init_training(tc.CATEGORICAL_COLUMNS, numerical_cols)
    X_train, X_test, y_train, y_test = train_test_split(
        preprocessed_train[tc.CATEGORICAL_COLUMNS + numerical_cols],
        preprocessed_train[tc.TARGET],
        test_size=0.33,
        random_state=88,
    )
    rf_model = training_pipeline.fit(X_train, y_train)

    return X_train.assign(Survived=y_train), X_test.assign(Survived=y_test), rf_model


def _strip_title(row):
    return row.split(",")[1].split(".")[0].replace(" ", "")


def preprocess(df):
    return (
        df.assign(Title=lambda x: x["Name"].apply(_strip_title))
        .assign(Fare=lambda x: x["Fare"].round(2))
        .drop(["Ticket", "Cabin", "Name", "PassengerId"], axis=1)
    )


def init_training(categorical_features, numerical_features):
    numeric_pipeline = Pipeline(steps=[("impute", SimpleImputer(strategy="mean")), ("scale", MinMaxScaler())])

    categorical_pipeline = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("one-hot", OneHotEncoder(handle_unknown="ignore", sparse=False)),
        ]
    )

    processor = ColumnTransformer(
        transformers=[
            ("number", numeric_pipeline, numerical_features),
            ("category", categorical_pipeline, categorical_features),
        ]
    )

    pipeline = Pipeline(steps=[("processor", processor), ("regressor", RandomForestClassifier(random_state=88))])
    return pipeline
