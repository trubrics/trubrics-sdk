LOCAL_TRAIN_FILENAME = "demo/data/preprocessed_train.csv"
LOCAL_TEST_FILENAME = "demo/data/preprocessed_test.csv"
LOCAL_MODEL_FILENAME = "demo/models/rf_model.pkl"
TARGET = "Survived"
CATEGORICAL_COLUMNS = ["Pclass", "Sex", "SibSp", "Parch", "Embarked", "Title"]
BUSINESS_COLUMNS = {
    "Pclass": "Ticket class",
    "SibSp": "Number of siblings / spouses aboard the Titanic",
    "Parch": "Number of parents / children aboard the Titanic",
    "Embarked": "Port of embarkation",
}
