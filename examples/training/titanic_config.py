TARGET = "Survived"
CATEGORICAL_COLUMNS = ["Sex", "Embarked", "Title"]

LOCAL_RAW_TRAIN_FILENAME = "examples/data/titanic_datasets/train.csv"

LOCAL_TRAIN_FILENAME = "examples/data/titanic_datasets/preprocessed_train.csv"
LOCAL_TEST_FILENAME = "examples/data/titanic_datasets/preprocessed_test.csv"
LOCAL_FI_FILENAME = "examples/data/titanic_datasets/feature_importance.json"
LOCAL_MODEL_FILENAME = "examples/models/rf_model.pkl"
BUSINESS_COLUMNS = {
    "Pclass": "Ticket class",
    "SibSp": "Number of siblings / spouses aboard the Titanic",
    "Parch": "Number of parents / children aboard the Titanic",
    "Embarked": "Port of embarkation",
}
