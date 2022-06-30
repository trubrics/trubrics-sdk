import json
import logging

import joblib
import pandas as pd
import titanic_config
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

logging.basicConfig(level=logging.INFO)


def main():
    train_df = pd.read_csv(titanic_config.LOCAL_RAW_TRAIN_FILENAME)
    preprocessed_train = train_df.pipe(preprocess)
    logging.info("Training data has been preprocessed.")

    numerical_cols = [
        col
        for col in preprocessed_train.columns
        if col not in titanic_config.CATEGORICAL_COLUMNS + [titanic_config.TARGET]
    ]

    training_pipeline = init_training(titanic_config.CATEGORICAL_COLUMNS, numerical_cols)
    X_train, X_test, y_train, y_test = train_test_split(
        preprocessed_train[titanic_config.CATEGORICAL_COLUMNS + numerical_cols],
        preprocessed_train[titanic_config.TARGET],
        test_size=0.33,
        random_state=88,
    )
    rf_model = training_pipeline.fit(X_train, y_train)
    logging.info(
        f"Model has been trained, with accuracy: {round(accuracy_score(rf_model.predict(X_test), y_test), 3)*100}%"
    )

    # save
    X_train.assign(Survived=y_train).to_csv(titanic_config.LOCAL_TRAIN_FILENAME, index=False)
    X_test.assign(Survived=y_test).to_csv(titanic_config.LOCAL_TEST_FILENAME, index=False)
    joblib.dump(rf_model, titanic_config.LOCAL_MODEL_FILENAME)

    feature_importance = get_feature_importance(rf_model, numerical_cols)
    with open(titanic_config.LOCAL_FI_FILENAME, "w") as file:
        file.write(json.dumps(feature_importance))


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


def get_feature_importance(model, numerical_cols):
    ohe_cols_raw = (
        model.named_steps["processor"].named_transformers_["category"].named_steps["one-hot"].get_feature_names_out()
    )
    ohe_cols = [col.replace("x0", "Sex").replace("x1", "Embarked").replace("x2", "Title") for col in ohe_cols_raw]
    return {
        key: value for key, value in zip(numerical_cols + ohe_cols, model.named_steps["regressor"].feature_importances_)
    }


if __name__ == "__main__":
    main()
