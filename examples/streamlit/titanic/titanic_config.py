TARGET = "Survived"
CATEGORICAL_COLUMNS = ["Sex", "Embarked", "Title"]
LOCAL_RAW_TRAIN_FILENAME = "trubrics/example/titanic_data.csv"
BUSINESS_COLUMNS = {
    "Pclass": "Ticket class",
    "SibSp": "Number of siblings / spouses aboard the Titanic",
    "Parch": "Number of parents / children aboard the Titanic",
    "Embarked": "Port of embarkation",
}
